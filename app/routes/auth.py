"""Authentication routes: register, login, logout, profile."""
from flask import (
    Blueprint, render_template, redirect, url_for, flash, request, abort
)
from flask_login import login_user, logout_user, login_required, current_user
from urllib.parse import urlparse

from ..extensions import db, limiter
from ..models import User, UserProgress, QuizAttempt, TrainingModule
from ..forms import LoginForm, RegistrationForm
from ..security import log_activity

auth_bp = Blueprint('auth', __name__)


def _is_safe_url(target):
    """Guard against open-redirects: only allow same-host http(s) targets."""
    if not target:
        return False
    ref = urlparse(request.host_url)
    test = urlparse(target)
    return test.scheme in ('', 'http', 'https') and ref.netloc == test.netloc


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Create a new employee account from the registration form."""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        existing = User.query.filter_by(email=form.email.data.lower().strip()).first()
        if existing:
            flash('An account with that email already exists.', 'danger')
        else:
            user = User(
                name=form.name.data.strip(),
                email=form.email.data.lower().strip(),
                department=(form.department.data or '').strip() or None,
                role='employee',
            )
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            log_activity('user_registered', user=user)
            flash('Account created. Please log in.', 'success')
            return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)


@auth_bp.route('/login', methods=['GET', 'POST'])
@limiter.limit('5 per minute', methods=['POST'])
def login():
    """Authenticate credentials, start a session, and redirect (rate-limited)."""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.home'))
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data.lower().strip()
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            log_activity('login_success', user=user)
            flash('Welcome back, %s!' % user.name, 'success')
            next_page = request.args.get('next')
            if next_page and _is_safe_url(next_page):
                return redirect(next_page)
            return redirect(url_for('dashboard.home'))
        else:
            log_activity('login_failed: %s' % email, user=user)
            flash('Invalid email or password.', 'danger')
    return render_template('auth/login.html', form=form)


@auth_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    """End the current user's session."""
    log_activity('logout')
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('dashboard.index'))


@auth_bp.route('/profile')
@login_required
def profile():
    """Show the current user's training progress and quiz-attempt history."""
    progress_records = UserProgress.query.filter_by(user_id=current_user.id).all()
    modules_total = TrainingModule.query.filter_by(is_active=True).count()
    completed = sum(1 for p in progress_records if p.status == 'completed')
    attempts = (
        QuizAttempt.query.filter_by(user_id=current_user.id)
        .order_by(QuizAttempt.created_at.desc())
        .all()
    )
    avg_score = round(sum(a.score for a in attempts) / len(attempts)) if attempts else 0
    progress_summary = {
        'modules_total': modules_total,
        'modules_completed': completed,
        'attempts_count': len(attempts),
        'avg_score': avg_score,
    }
    return render_template(
        'profile.html',
        user=current_user,
        progress_summary=progress_summary,
        attempts=attempts,
    )
