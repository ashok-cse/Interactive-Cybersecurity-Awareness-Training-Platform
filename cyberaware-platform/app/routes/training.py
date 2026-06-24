"""Training routes: modules, detail, quiz, results."""
from flask import (
    Blueprint, render_template, redirect, url_for, flash, request, abort,
    current_app, session
)
from flask_login import login_required, current_user

from ..extensions import db
from ..models import TrainingModule, QuizQuestion, QuizAttempt, UserProgress
from ..security import log_activity
from ..utils import utcnow

training_bp = Blueprint('training', __name__, url_prefix='/training')


def _get_or_create_progress(user_id, module_id):
    progress = UserProgress.query.filter_by(
        user_id=user_id, module_id=module_id
    ).first()
    if progress is None:
        progress = UserProgress(
            user_id=user_id, module_id=module_id,
            status='not_started', completion_percentage=0,
        )
        db.session.add(progress)
        db.session.commit()
    return progress


@training_bp.route('/')
@login_required
def modules():
    mods = (
        TrainingModule.query.filter_by(is_active=True)
        .order_by(TrainingModule.order, TrainingModule.id)
        .all()
    )
    prog_map = {
        p.module_id: p
        for p in UserProgress.query.filter_by(user_id=current_user.id).all()
    }
    rows = []
    for m in mods:
        p = prog_map.get(m.id)
        rows.append({
            'module': m,
            'status': p.status if p else 'not_started',
            'percentage': p.completion_percentage if p else 0,
        })
    return render_template('training/modules.html', modules=rows)


@training_bp.route('/module/<int:module_id>')
@login_required
def module_detail(module_id):
    module = TrainingModule.query.get_or_404(module_id)
    progress = _get_or_create_progress(current_user.id, module_id)
    has_quiz = QuizQuestion.query.filter_by(module_id=module_id).count() > 0
    progress_view = {
        'status': progress.status,
        'percentage': progress.completion_percentage,
    }
    return render_template(
        'training/module_detail.html',
        module=module,
        progress=progress_view,
        has_quiz=has_quiz,
    )


@training_bp.route('/module/<int:module_id>/start', methods=['POST'])
@login_required
def start_module(module_id):
    TrainingModule.query.get_or_404(module_id)
    progress = _get_or_create_progress(current_user.id, module_id)
    if progress.status == 'not_started':
        progress.status = 'in_progress'
        if progress.completion_percentage < 50:
            progress.completion_percentage = 50
        db.session.commit()
        log_activity('module_started: %d' % module_id)
    return redirect(url_for('training.module_detail', module_id=module_id))


@training_bp.route('/module/<int:module_id>/quiz', methods=['GET', 'POST'])
@login_required
def quiz(module_id):
    module = TrainingModule.query.get_or_404(module_id)
    questions = (
        QuizQuestion.query.filter_by(module_id=module_id)
        .order_by(QuizQuestion.id)
        .all()
    )
    if not questions:
        flash('This module has no quiz yet.', 'info')
        return redirect(url_for('training.module_detail', module_id=module_id))

    if request.method == 'POST':
        total = len(questions)
        correct = 0
        answers = {}
        for q in questions:
            answer = (request.form.get('q_%d' % q.id) or '').strip().upper()
            answers[str(q.id)] = answer
            if answer == q.correct_answer:
                correct += 1
        score = round(correct / total * 100)
        threshold = current_app.config.get('PASS_THRESHOLD', 70)
        passed = score >= threshold

        attempt = QuizAttempt(
            user_id=current_user.id,
            module_id=module_id,
            score=score,
            passed=passed,
            created_at=utcnow(),
        )
        db.session.add(attempt)

        progress = _get_or_create_progress(current_user.id, module_id)
        if passed:
            progress.status = 'completed'
            progress.completion_percentage = 100
            progress.completed_at = utcnow()
        elif progress.status == 'not_started':
            progress.status = 'in_progress'
            progress.completion_percentage = max(progress.completion_percentage, 50)
        db.session.commit()

        # Stash submitted answers so the result page can show per-question detail.
        session['quiz_answers_%d' % attempt.id] = answers

        log_activity(
            'quiz_attempt: module=%d score=%d passed=%s'
            % (module_id, score, passed)
        )
        return redirect(url_for('training.quiz_result', attempt_id=attempt.id))

    return render_template('training/quiz.html', module=module, questions=questions)


@training_bp.route('/quiz/result/<int:attempt_id>')
@login_required
def quiz_result(attempt_id):
    attempt = QuizAttempt.query.get_or_404(attempt_id)
    if attempt.user_id != current_user.id and not (
        current_user.is_admin or current_user.is_trainer
    ):
        abort(403)
    module = TrainingModule.query.get_or_404(attempt.module_id)
    questions = (
        QuizQuestion.query.filter_by(module_id=module.id)
        .order_by(QuizQuestion.id)
        .all()
    )
    answers = session.get('quiz_answers_%d' % attempt.id, {})
    results = []
    for q in questions:
        options = {
            'A': q.option_a,
            'B': q.option_b,
            'C': q.option_c,
            'D': q.option_d,
        }
        your_answer = answers.get(str(q.id)) or None
        is_correct = (your_answer == q.correct_answer) if your_answer is not None else None
        results.append({
            'question': q.question,
            'your_answer': your_answer,
            'correct_answer': q.correct_answer,
            'is_correct': is_correct,
            'explanation': q.explanation,
            'options': options,
        })
    return render_template(
        'training/quiz_result.html',
        attempt=attempt,
        module=module,
        score=attempt.score,
        passed=attempt.passed,
        results=results,
    )
