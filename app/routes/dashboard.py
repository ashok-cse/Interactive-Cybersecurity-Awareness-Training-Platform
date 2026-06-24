"""Dashboard routes: public landing + role-dispatched dashboard."""
from flask import Blueprint, render_template
from flask_login import login_required, current_user

from ..extensions import db
from ..models import (
    User, TrainingModule, QuizAttempt, UserProgress,
    PhishingCampaign, PhishingAssignment, ActivityLog
)

dashboard_bp = Blueprint('dashboard', __name__)


def _module_progress_list(user):
    """Return list of {module, status, percentage} for active modules."""
    modules = (
        TrainingModule.query.filter_by(is_active=True)
        .order_by(TrainingModule.order, TrainingModule.id)
        .all()
    )
    prog_map = {
        p.module_id: p
        for p in UserProgress.query.filter_by(user_id=user.id).all()
    }
    rows = []
    for m in modules:
        p = prog_map.get(m.id)
        rows.append({
            'module': m,
            'status': p.status if p else 'not_started',
            'percentage': p.completion_percentage if p else 0,
        })
    return rows


def _employee_dashboard():
    user = current_user
    module_rows = _module_progress_list(user)
    modules_total = len(module_rows)
    modules_completed = sum(1 for r in module_rows if r['status'] == 'completed')

    attempts = (
        QuizAttempt.query.filter_by(user_id=user.id)
        .order_by(QuizAttempt.created_at.desc())
        .all()
    )
    avg_score = round(sum(a.score for a in attempts) / len(attempts)) if attempts else 0

    assignments = (
        PhishingAssignment.query.filter_by(user_id=user.id)
        .order_by(PhishingAssignment.id.desc())
        .all()
    )
    phishing_pending = sum(1 for a in assignments if a.responded_at is None)

    stats = {
        'modules_total': modules_total,
        'modules_completed': modules_completed,
        'avg_score': avg_score,
        'phishing_pending': phishing_pending,
    }
    return render_template(
        'dashboard/employee.html',
        stats=stats,
        modules=module_rows,
        attempts=attempts[:5],
        assignments=assignments,
    )


def _module_stats():
    """Per-module completion rate and average score across all users."""
    total_users = User.query.filter_by(role='employee').count()
    modules = (
        TrainingModule.query.filter_by(is_active=True)
        .order_by(TrainingModule.order, TrainingModule.id)
        .all()
    )
    rows = []
    for m in modules:
        completed = UserProgress.query.filter_by(
            module_id=m.id, status='completed'
        ).count()
        completion_rate = round(completed / total_users * 100) if total_users else 0
        attempts = QuizAttempt.query.filter_by(module_id=m.id).all()
        avg_score = round(sum(a.score for a in attempts) / len(attempts)) if attempts else 0
        rows.append({
            'module': m,
            'completion_rate': completion_rate,
            'avg_score': avg_score,
        })
    return rows


def _user_progress_summaries():
    users = User.query.filter_by(role='employee').order_by(User.name).all()
    modules_total = TrainingModule.query.filter_by(is_active=True).count()
    summaries = []
    for u in users:
        completed = UserProgress.query.filter_by(
            user_id=u.id, status='completed'
        ).count()
        attempts = QuizAttempt.query.filter_by(user_id=u.id).all()
        avg_score = round(sum(a.score for a in attempts) / len(attempts)) if attempts else 0
        completion_rate = round(completed / modules_total * 100) if modules_total else 0
        summaries.append({
            'user': u,
            'modules_completed': completed,
            'modules_total': modules_total,
            'completion_rate': completion_rate,
            'avg_score': avg_score,
        })
    return summaries


def _overall_completion_rate():
    total_users = User.query.filter_by(role='employee').count()
    modules_total = TrainingModule.query.filter_by(is_active=True).count()
    denom = total_users * modules_total
    if not denom:
        return 0
    completed = UserProgress.query.filter_by(status='completed').count()
    return round(completed / denom * 100)


def _trainer_dashboard():
    total_users = User.query.filter_by(role='employee').count()
    attempts = QuizAttempt.query.all()
    avg_score = round(sum(a.score for a in attempts) / len(attempts)) if attempts else 0
    stats = {
        'total_users': total_users,
        'completion_rate': _overall_completion_rate(),
        'avg_score': avg_score,
        'total_campaigns': PhishingCampaign.query.count(),
    }
    return render_template(
        'dashboard/trainer.html',
        stats=stats,
        users=_user_progress_summaries(),
        module_stats=_module_stats(),
    )


def _admin_dashboard():
    stats = {
        'total_users': User.query.count(),
        'total_modules': TrainingModule.query.count(),
        'total_campaigns': PhishingCampaign.query.count(),
        'completion_rate': _overall_completion_rate(),
    }
    recent_logs = (
        ActivityLog.query.order_by(ActivityLog.created_at.desc())
        .limit(20)
        .all()
    )
    return render_template(
        'dashboard/admin.html',
        stats=stats,
        recent_logs=recent_logs,
        module_stats=_module_stats(),
    )


@dashboard_bp.route('/')
def index():
    return render_template('index.html')


@dashboard_bp.route('/dashboard')
@login_required
def home():
    if current_user.is_admin:
        return _admin_dashboard()
    if current_user.is_trainer:
        return _trainer_dashboard()
    return _employee_dashboard()
