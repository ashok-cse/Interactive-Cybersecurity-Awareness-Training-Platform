"""Small shared helpers."""
from datetime import datetime, timezone


def utcnow():
    """Return the current UTC time as a naive datetime.

    Behaviour-identical to the deprecated ``datetime.utcnow()`` (naive UTC), but
    built on the non-deprecated ``datetime.now(timezone.utc)``. Kept naive so it
    stays consistent with the naive ``DateTime`` columns stored by SQLAlchemy.
    """
    return datetime.now(timezone.utc).replace(tzinfo=None)
