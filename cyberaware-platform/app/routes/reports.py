"""CSV report export routes (staff only)."""
import csv
import io

from flask import Blueprint, Response
from flask_login import login_required

from ..models import (
    User, TrainingModule, QuizAttempt, UserProgress,
    PhishingCampaign, PhishingAssignment
)
from ..security import staff_required

reports_bp = Blueprint('reports', __name__, url_prefix='/reports')


def _csv_response(filename, header, rows):
    buf = io.StringIO()
    writer = csv.writer(buf)
    writer.writerow(header)
    for row in rows:
        writer.writerow(row)
    output = buf.getvalue()
    buf.close()
    return Response(
        output,
        mimetype='text/csv',
        headers={'Content-Disposition': 'attachment; filename="%s"' % filename},
    )


@reports_bp.route('/user-progress.csv')
@login_required
@staff_required
def user_progress_csv():
    header = [
        'User ID', 'Name', 'Email', 'Department', 'Role',
        'Module', 'Status', 'Completion %', 'Completed At',
    ]
    rows = []
    records = (
        UserProgress.query.join(User, UserProgress.user_id == User.id)
        .join(TrainingModule, UserProgress.module_id == TrainingModule.id)
        .order_by(User.name)
        .all()
    )
    for p in records:
        u = p.user
        m = p.module
        rows.append([
            u.id, u.name, u.email, u.department or '', u.role,
            m.title, p.status, p.completion_percentage,
            p.completed_at.isoformat() if p.completed_at else '',
        ])
    return _csv_response('user-progress.csv', header, rows)


@reports_bp.route('/quiz-scores.csv')
@login_required
@staff_required
def quiz_scores_csv():
    header = ['Attempt ID', 'User', 'Email', 'Module', 'Score', 'Passed', 'Date']
    rows = []
    attempts = (
        QuizAttempt.query.order_by(QuizAttempt.created_at.desc()).all()
    )
    for a in attempts:
        u = a.user
        m = a.module
        rows.append([
            a.id,
            u.name if u else '',
            u.email if u else '',
            m.title if m else '',
            a.score,
            'Yes' if a.passed else 'No',
            a.created_at.isoformat() if a.created_at else '',
        ])
    return _csv_response('quiz-scores.csv', header, rows)


@reports_bp.route('/phishing.csv')
@login_required
@staff_required
def phishing_csv():
    header = [
        'Assignment ID', 'User', 'Email', 'Campaign', 'Is Phishing',
        'User Response', 'Correct', 'Responded At',
    ]
    rows = []
    assignments = (
        PhishingAssignment.query
        .join(User, PhishingAssignment.user_id == User.id)
        .join(PhishingCampaign, PhishingAssignment.campaign_id == PhishingCampaign.id)
        .order_by(PhishingAssignment.id)
        .all()
    )
    for a in assignments:
        u = a.user
        c = a.campaign
        rows.append([
            a.id,
            u.name if u else '',
            u.email if u else '',
            c.title if c else '',
            'Yes' if (c and c.is_phishing) else 'No',
            a.user_response or 'pending',
            ('Yes' if a.is_correct else 'No') if a.responded_at else '',
            a.responded_at.isoformat() if a.responded_at else '',
        ])
    return _csv_response('phishing.csv', header, rows)
