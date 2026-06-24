"""Admin & trainer routes: users, assignments, campaigns, analytics, reports."""
from flask import (
    Blueprint, render_template, redirect, url_for, flash, request
)
from flask_login import login_required, current_user

from ..extensions import db
from ..models import (
    User, TrainingModule, QuizAttempt, UserProgress,
    PhishingCampaign, PhishingAssignment
)
from ..forms import CampaignForm
from ..security import admin_required, staff_required, log_activity

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


@admin_bp.route('/users')
@login_required
@admin_required
def users():
    all_users = User.query.order_by(User.role, User.name).all()
    return render_template('admin/users.html', users=all_users)


@admin_bp.route('/assign-modules', methods=['GET', 'POST'])
@login_required
@staff_required
def assign_modules():
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


@admin_bp.route('/campaigns', methods=['GET', 'POST'])
@login_required
@staff_required
def campaigns():
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
    return render_template('admin/analytics.html', chart_data=_build_chart_data())


@admin_bp.route('/reports')
@login_required
@staff_required
def reports():
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
