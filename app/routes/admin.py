"""Admin & trainer routes: users, assignments, campaigns, analytics, reports."""
from flask import (
    Blueprint, render_template, redirect, url_for, flash, request, abort
)
from flask_login import login_required, current_user

from ..extensions import db
from ..models import (
    User, TrainingModule, QuizQuestion, QuizAttempt, UserProgress,
    PhishingCampaign, PhishingAssignment
)
from ..forms import CampaignForm, ModuleForm, QuestionForm
from ..security import admin_required, staff_required, log_activity
from ..utils import sanitize_html

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


@admin_bp.route('/users')
@login_required
@admin_required
def users():
    """List all users grouped by role (admin only)."""
    all_users = User.query.order_by(User.role, User.name).all()
    return render_template('admin/users.html', users=all_users)


@admin_bp.route('/assign-modules', methods=['GET', 'POST'])
@login_required
@staff_required
def assign_modules():
    """Assign one or more training modules to an employee, skipping duplicates."""
    employees = User.query.filter_by(role='employee').order_by(User.name).all()
    modules = (
        TrainingModule.query.filter_by(is_active=True)
        .order_by(TrainingModule.order, TrainingModule.id)
        .all()
    )
    if request.method == 'POST':
        user_id = request.form.get('user_id', type=int)
        module_ids = request.form.getlist('module_ids', type=int)
        target = db.session.get(User, user_id) if user_id else None
        if not target:
            flash('Please select a valid user.', 'danger')
        elif not module_ids:
            flash('Please select at least one module.', 'danger')
        else:
            created = 0
            for mid in module_ids:
                existing = UserProgress.query.filter_by(
                    user_id=target.id, module_id=mid
                ).first()
                if not existing:
                    db.session.add(UserProgress(
                        user_id=target.id, module_id=mid,
                        status='not_started', completion_percentage=0,
                    ))
                    created += 1
            db.session.commit()
            log_activity('assigned_modules: user=%d count=%d' % (target.id, created))
            flash('Assigned %d module(s) to %s.' % (created, target.name), 'success')
        return redirect(url_for('admin.assign_modules'))
    return render_template(
        'admin/assign_modules.html',
        users=employees,
        modules=modules,
    )


# ---------------------------------------------------------------------------
# Content management: training modules and quiz questions.
# ---------------------------------------------------------------------------

@admin_bp.route('/modules')
@login_required
@staff_required
def modules():
    """List every training module with its quiz-question count (staff only)."""
    all_modules = (
        TrainingModule.query
        .order_by(TrainingModule.order, TrainingModule.id)
        .all()
    )
    counts = {
        m.id: QuizQuestion.query.filter_by(module_id=m.id).count()
        for m in all_modules
    }
    return render_template(
        'admin/modules.html', modules=all_modules, counts=counts
    )


@admin_bp.route('/modules/new', methods=['GET', 'POST'])
@login_required
@staff_required
def module_new():
    """Create a new training module; sanitizes authored HTML content."""
    form = ModuleForm()
    if form.validate_on_submit():
        module = TrainingModule(
            title=form.title.data.strip(),
            description=(form.description.data or '').strip(),
            category=(form.category.data or '').strip(),
            content=sanitize_html(form.content.data),
            order=form.order.data or 0,
            is_active=form.is_active.data,
        )
        db.session.add(module)
        db.session.commit()
        log_activity('module_created: %d' % module.id)
        flash('Module "%s" created.' % module.title, 'success')
        return redirect(url_for('admin.modules'))
    return render_template(
        'admin/module_form.html', form=form, mode='new', module=None
    )


@admin_bp.route('/modules/<int:module_id>/edit', methods=['GET', 'POST'])
@login_required
@staff_required
def module_edit(module_id):
    """Edit an existing training module; re-sanitizes content on save."""
    module = db.session.get(TrainingModule, module_id)
    if not module:
        abort(404)
    form = ModuleForm(obj=module)
    if form.validate_on_submit():
        module.title = form.title.data.strip()
        module.description = (form.description.data or '').strip()
        module.category = (form.category.data or '').strip()
        module.content = sanitize_html(form.content.data)
        module.order = form.order.data or 0
        module.is_active = form.is_active.data
        db.session.commit()
        log_activity('module_updated: %d' % module.id)
        flash('Module "%s" updated.' % module.title, 'success')
        return redirect(url_for('admin.modules'))
    return render_template(
        'admin/module_form.html', form=form, mode='edit', module=module
    )


@admin_bp.route('/modules/<int:module_id>/delete', methods=['POST'])
@login_required
@staff_required
def module_delete(module_id):
    """Delete a module (cascades to its questions and progress rows)."""
    module = db.session.get(TrainingModule, module_id)
    if not module:
        abort(404)
    title = module.title
    db.session.delete(module)
    db.session.commit()
    log_activity('module_deleted: %d' % module_id)
    flash('Module "%s" deleted.' % title, 'success')
    return redirect(url_for('admin.modules'))


@admin_bp.route('/modules/<int:module_id>/questions')
@login_required
@staff_required
def module_questions(module_id):
    """List all quiz questions for a module (staff only)."""
    module = db.session.get(TrainingModule, module_id)
    if not module:
        abort(404)
    questions = (
        QuizQuestion.query.filter_by(module_id=module_id)
        .order_by(QuizQuestion.id)
        .all()
    )
    return render_template(
        'admin/questions.html', module=module, questions=questions
    )


@admin_bp.route('/modules/<int:module_id>/questions/new', methods=['GET', 'POST'])
@login_required
@staff_required
def question_new(module_id):
    """Add a quiz question to a module."""
    module = db.session.get(TrainingModule, module_id)
    if not module:
        abort(404)
    form = QuestionForm()
    if form.validate_on_submit():
        question = QuizQuestion(
            module_id=module.id,
            question=form.question.data.strip(),
            option_a=form.option_a.data.strip(),
            option_b=form.option_b.data.strip(),
            option_c=form.option_c.data.strip(),
            option_d=form.option_d.data.strip(),
            correct_answer=form.correct_answer.data,
            explanation=(form.explanation.data or '').strip(),
        )
        db.session.add(question)
        db.session.commit()
        log_activity('question_created: module=%d q=%d' % (module.id, question.id))
        flash('Question added.', 'success')
        return redirect(url_for('admin.module_questions', module_id=module.id))
    return render_template(
        'admin/question_form.html',
        form=form, mode='new', module=module, question=None,
    )


@admin_bp.route('/questions/<int:question_id>/edit', methods=['GET', 'POST'])
@login_required
@staff_required
def question_edit(question_id):
    """Edit an existing quiz question."""
    question = db.session.get(QuizQuestion, question_id)
    if not question:
        abort(404)
    module = db.session.get(TrainingModule, question.module_id)
    form = QuestionForm(obj=question)
    if form.validate_on_submit():
        question.question = form.question.data.strip()
        question.option_a = form.option_a.data.strip()
        question.option_b = form.option_b.data.strip()
        question.option_c = form.option_c.data.strip()
        question.option_d = form.option_d.data.strip()
        question.correct_answer = form.correct_answer.data
        question.explanation = (form.explanation.data or '').strip()
        db.session.commit()
        log_activity('question_updated: %d' % question.id)
        flash('Question updated.', 'success')
        return redirect(url_for('admin.module_questions', module_id=question.module_id))
    return render_template(
        'admin/question_form.html',
        form=form, mode='edit', module=module, question=question,
    )


@admin_bp.route('/questions/<int:question_id>/delete', methods=['POST'])
@login_required
@staff_required
def question_delete(question_id):
    """Delete a single quiz question."""
    question = db.session.get(QuizQuestion, question_id)
    if not question:
        abort(404)
    module_id = question.module_id
    db.session.delete(question)
    db.session.commit()
    log_activity('question_deleted: %d' % question_id)
    flash('Question deleted.', 'success')
    return redirect(url_for('admin.module_questions', module_id=module_id))


@admin_bp.route('/campaigns', methods=['GET', 'POST'])
@login_required
@staff_required
def campaigns():
    """Create a phishing campaign (POST) and list existing campaigns (GET)."""
    form = CampaignForm()
    if form.validate_on_submit():
        campaign = PhishingCampaign(
            title=form.title.data.strip(),
            subject=form.subject.data.strip(),
            sender_name=form.sender_name.data.strip(),
            sender_email=form.sender_email.data.strip(),
            body=form.body.data,
            red_flags=form.red_flags.data or '',
            difficulty=form.difficulty.data,
            is_phishing=form.is_phishing.data,
            created_by=current_user.id,
        )
        db.session.add(campaign)
        db.session.commit()
        log_activity('campaign_created: %d' % campaign.id)
        flash('Campaign "%s" created.' % campaign.title, 'success')
        return redirect(url_for('admin.campaigns'))

    all_campaigns = (
        PhishingCampaign.query.order_by(PhishingCampaign.created_at.desc()).all()
    )
    employees = User.query.filter_by(role='employee').order_by(User.name).all()
    return render_template(
        'admin/campaigns.html',
        campaigns=all_campaigns,
        users=employees,
        form=form,
    )


@admin_bp.route('/campaigns/assign', methods=['POST'])
@login_required
@staff_required
def assign_campaign():
    """Assign a phishing campaign to selected users, skipping duplicates."""
    campaign_id = request.form.get('campaign_id', type=int)
    user_ids = request.form.getlist('user_ids', type=int)
    campaign = db.session.get(PhishingCampaign, campaign_id) if campaign_id else None
    if not campaign:
        flash('Please select a valid campaign.', 'danger')
    elif not user_ids:
        flash('Please select at least one user.', 'danger')
    else:
        created = 0
        for uid in user_ids:
            existing = PhishingAssignment.query.filter_by(
                campaign_id=campaign.id, user_id=uid
            ).first()
            if not existing:
                db.session.add(PhishingAssignment(
                    campaign_id=campaign.id, user_id=uid
                ))
                created += 1
        db.session.commit()
        log_activity('campaign_assigned: campaign=%d count=%d' % (campaign.id, created))
        flash('Assigned campaign to %d user(s).' % created, 'success')
    return redirect(url_for('admin.campaigns'))


def _build_chart_data():
    """Aggregate metrics for the analytics charts: per-module completion and
    average scores, overall pass/fail, and phishing correct/incorrect/pending."""
    modules = (
        TrainingModule.query.filter_by(is_active=True)
        .order_by(TrainingModule.order, TrainingModule.id)
        .all()
    )
    total_users = User.query.filter_by(role='employee').count()

    completion_labels, completion_values = [], []
    score_labels, score_values = [], []
    for m in modules:
        completed = UserProgress.query.filter_by(
            module_id=m.id, status='completed'
        ).count()
        rate = round(completed / total_users * 100) if total_users else 0
        completion_labels.append(m.title)
        completion_values.append(rate)

        attempts = QuizAttempt.query.filter_by(module_id=m.id).all()
        avg = round(sum(a.score for a in attempts) / len(attempts)) if attempts else 0
        score_labels.append(m.title)
        score_values.append(avg)

    all_attempts = QuizAttempt.query.all()
    passed = sum(1 for a in all_attempts if a.passed)
    failed = len(all_attempts) - passed

    p_assignments = PhishingAssignment.query.all()
    p_correct = sum(1 for a in p_assignments if a.responded_at and a.is_correct)
    p_incorrect = sum(1 for a in p_assignments if a.responded_at and not a.is_correct)
    p_pending = sum(1 for a in p_assignments if a.responded_at is None)

    return {
        'completion': {'labels': completion_labels, 'values': completion_values},
        'avg_scores': {'labels': score_labels, 'values': score_values},
        'pass_fail': {'passed': passed, 'failed': failed},
        'phishing': {'correct': p_correct, 'incorrect': p_incorrect, 'pending': p_pending},
    }


@admin_bp.route('/analytics')
@login_required
@staff_required
def analytics():
    """Render the analytics dashboard with aggregated chart data."""
    return render_template('admin/analytics.html', chart_data=_build_chart_data())


@admin_bp.route('/reports')
@login_required
@staff_required
def reports():
    """Render the summary report: user/module counts, quiz and phishing metrics."""
    total_users = User.query.count()
    total_employees = User.query.filter_by(role='employee').count()
    total_modules = TrainingModule.query.filter_by(is_active=True).count()
    completed_progress = UserProgress.query.filter_by(status='completed').count()
    attempts = QuizAttempt.query.all()
    avg_score = round(sum(a.score for a in attempts) / len(attempts)) if attempts else 0
    pass_rate = (
        round(sum(1 for a in attempts if a.passed) / len(attempts) * 100)
        if attempts else 0
    )
    p_assignments = PhishingAssignment.query.all()
    p_responded = [a for a in p_assignments if a.responded_at is not None]
    p_detect_rate = (
        round(sum(1 for a in p_responded if a.is_correct) / len(p_responded) * 100)
        if p_responded else 0
    )

    report_summary = {
        'total_users': total_users,
        'total_employees': total_employees,
        'total_modules': total_modules,
        'completed_progress': completed_progress,
        'total_attempts': len(attempts),
        'avg_score': avg_score,
        'pass_rate': pass_rate,
        'total_campaigns': PhishingCampaign.query.count(),
        'phishing_assignments': len(p_assignments),
        'phishing_responded': len(p_responded),
        'phishing_detect_rate': p_detect_rate,
    }
    return render_template('admin/reports.html', report_summary=report_summary)
