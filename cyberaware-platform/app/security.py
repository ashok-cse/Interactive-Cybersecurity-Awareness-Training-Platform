"""Security helpers: role decorators and activity logging."""
from functools import wraps

from flask import abort, request
from flask_login import current_user

from .extensions import db, login_manager
from .models import ActivityLog


def roles_required(*roles):
    """Restrict a view to the given roles.

    Anonymous users are redirected to login (401 -> handled by login_manager),
    authenticated users without an allowed role get a 403.
    """
    def decorator(view):
        @wraps(view)
        def wrapped(*args, **kwargs):
            if not current_user.is_authenticated:
                # Redirect to login (preserving next) like @login_required.
                return login_manager.unauthorized()
            if roles and current_user.role not in roles:
                abort(403)
            return view(*args, **kwargs)
        return wrapped
    return decorator


def admin_required(view):
    return roles_required('admin')(view)


def staff_required(view):
    """Admin or trainer."""
    return roles_required('admin', 'trainer')(view)


def log_activity(action, user=None):
    """Persist an ActivityLog entry with the requesting IP address."""
    if user is None and current_user.is_authenticated:
        user = current_user
    user_id = getattr(user, 'id', None)
    try:
        ip = request.remote_addr
    except RuntimeError:
        ip = None
    entry = ActivityLog(user_id=user_id, action=action, ip_address=ip)
    db.session.add(entry)
    db.session.commit()
    return entry
