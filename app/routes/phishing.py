"""Phishing simulation routes: inbox, email detail, respond, result."""
from flask import (
    Blueprint, render_template, redirect, url_for, flash, request, abort
)
from flask_login import login_required, current_user

from ..extensions import db
from ..models import PhishingAssignment, PhishingCampaign
from ..security import log_activity
from ..utils import utcnow

phishing_bp = Blueprint('phishing', __name__, url_prefix='/phishing')


def _get_owned_assignment(assignment_id):
    """Load an assignment, aborting 403 if it doesn't belong to the current user."""
    assignment = PhishingAssignment.query.get_or_404(assignment_id)
    if assignment.user_id != current_user.id:
        abort(403)
    return assignment


@phishing_bp.route('/')
@login_required
def inbox():
    """List the phishing-simulation emails assigned to the current user."""
    assignments = (
        PhishingAssignment.query.filter_by(user_id=current_user.id)
        .order_by(PhishingAssignment.id.desc())
        .all()
    )
    return render_template('phishing/inbox.html', assignments=assignments)


@phishing_bp.route('/email/<int:assignment_id>')
@login_required
def email_detail(assignment_id):
    """Show a simulated email so the user can judge it; skip to result if answered."""
    assignment = _get_owned_assignment(assignment_id)
    if assignment.responded_at is not None:
        return redirect(url_for('phishing.result', assignment_id=assignment_id))
    campaign = PhishingCampaign.query.get_or_404(assignment.campaign_id)
    return render_template(
        'phishing/email_detail.html',
        assignment=assignment,
        campaign=campaign,
    )


@phishing_bp.route('/email/<int:assignment_id>/respond', methods=['POST'])
@login_required
def respond(assignment_id):
    """Record the user's phishing/legitimate verdict and score it (once)."""
    assignment = _get_owned_assignment(assignment_id)
    campaign = PhishingCampaign.query.get_or_404(assignment.campaign_id)

    response = (request.form.get('response') or '').strip().lower()
    if response not in ('phishing', 'legitimate'):
        flash('Please choose a valid response.', 'danger')
        return redirect(url_for('phishing.email_detail', assignment_id=assignment_id))

    if assignment.responded_at is None:
        correct_response = campaign.correct_response
        assignment.user_response = response
        assignment.is_correct = (response == correct_response)
        assignment.responded_at = utcnow()
        db.session.commit()
        log_activity(
            'phishing_response: assignment=%d response=%s correct=%s'
            % (assignment_id, response, assignment.is_correct)
        )
    return redirect(url_for('phishing.result', assignment_id=assignment_id))


@phishing_bp.route('/email/<int:assignment_id>/result')
@login_required
def result(assignment_id):
    """Show whether the user's verdict was correct, with the email's red flags."""
    assignment = _get_owned_assignment(assignment_id)
    campaign = PhishingCampaign.query.get_or_404(assignment.campaign_id)
    if assignment.responded_at is None:
        return redirect(url_for('phishing.email_detail', assignment_id=assignment_id))
    correct_label = 'Phishing' if campaign.is_phishing else 'Legitimate'
    return render_template(
        'phishing/result.html',
        assignment=assignment,
        campaign=campaign,
        is_correct=bool(assignment.is_correct),
        red_flags=campaign.red_flags_list(),
        correct_label=correct_label,
    )
