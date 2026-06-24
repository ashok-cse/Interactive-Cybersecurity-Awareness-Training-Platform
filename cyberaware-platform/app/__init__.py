"""Application factory for the CyberAware platform."""
import os
from datetime import datetime, timedelta

from flask import Flask, render_template, session
from dotenv import load_dotenv

from .config import get_config
from .extensions import db, login_manager, csrf, limiter
from .utils import utcnow

load_dotenv()


def create_app(config_name=None):
    app = Flask(__name__)
    config_class = get_config(config_name)
    app.config.from_object(config_class)

    # Ensure instance folder exists for default sqlite path.
    try:
        os.makedirs(app.instance_path, exist_ok=True)
        os.makedirs(
            os.path.join(os.path.dirname(app.root_path), 'instance'),
            exist_ok=True,
        )
    except OSError:
        pass

    # Init extensions.
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    limiter.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    # Session: permanent + idle timeout enforcement.
    @app.before_request
    def _session_management():
        session.permanent = True
        timeout = app.config.get('SESSION_TIMEOUT_MINUTES', 30)
        now = utcnow()
        last_active = session.get('last_active')
        if last_active:
            try:
                last_dt = datetime.fromisoformat(last_active)
            except (ValueError, TypeError):
                last_dt = now
            if now - last_dt > timedelta(minutes=timeout):
                from flask_login import logout_user
                logout_user()
                session.clear()
        session['last_active'] = now.isoformat()

    # Security headers.
    @app.after_request
    def _security_headers(response):
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['Referrer-Policy'] = 'no-referrer-when-downgrade'
        response.headers['Content-Security-Policy'] = (
            "default-src 'self'; "
            "script-src 'self' https://cdn.jsdelivr.net 'unsafe-inline'; "
            "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "
            "img-src 'self' data:;"
        )
        return response

    # Register blueprints.
    from .routes.auth import auth_bp
    from .routes.dashboard import dashboard_bp
    from .routes.training import training_bp
    from .routes.phishing import phishing_bp
    from .routes.admin import admin_bp
    from .routes.reports import reports_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(training_bp)
    app.register_blueprint(phishing_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(reports_bp)

    # Error handlers.
    @app.errorhandler(403)
    def _forbidden(e):
        return render_template('errors/403.html'), 403

    @app.errorhandler(404)
    def _not_found(e):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def _server_error(e):
        db.session.rollback()
        return render_template('errors/500.html'), 500

    # Self-initialize tables.
    with app.app_context():
        db.create_all()

    # CLI seed command.
    @app.cli.command('seed')
    def seed_command():
        """Populate the database with demo data."""
        import sys
        sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
        from seed import seed
        seed()
        print('Seed complete.')

    return app
