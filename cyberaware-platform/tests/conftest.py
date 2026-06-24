"""
Pytest configuration and shared fixtures for the CyberAware platform test suite.

TestingConfig key settings (from app/config.py):
  - TESTING = True
  - WTF_CSRF_ENABLED = False   (no CSRF tokens needed in test requests)
  - SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
  - RATELIMIT_ENABLED = False

StaticPool is injected so every connection (outer app-context session AND
the test-client's per-request session) shares the same in-memory SQLite
database – otherwise each new SQLite connection opens a blank :memory: DB.
"""

import pytest
from sqlalchemy.pool import StaticPool

from app import create_app
from app.extensions import db as _db
from app.models import (
    User,
    TrainingModule,
    QuizQuestion,
    UserProgress,
    PhishingCampaign,
    PhishingAssignment,
)


# ---------------------------------------------------------------------------
# Plain helper functions (not fixtures) – importable by any test module
# ---------------------------------------------------------------------------

def _make_user(
    email: str,
    password: str,
    name: str = "Test User",
    role: str = "employee",
    department: str = "IT",
) -> User:
    """Create, hash-password, persist, and return a User.

    Caller must be inside an active app context (guaranteed when called from
    a fixture or test that depends on the ``app`` fixture).
    """
    user = User(name=name, email=email, role=role, department=department)
    user.set_password(password)
    _db.session.add(user)
    _db.session.commit()
    return user


def do_login(client, email: str, password: str):
    """POST to /login; returns the raw response (redirects NOT followed).

    CSRF is disabled in TestingConfig so no token is required.
    """
    return client.post(
        "/login",
        data={"email": email, "password": password},
        follow_redirects=False,
    )


# ---------------------------------------------------------------------------
# Core fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(scope="function")
def app():
    """Fresh Flask app with an isolated in-memory SQLite DB per test.

    StaticPool ensures the same physical SQLite connection is reused by
    both the outer app-context session and requests issued via the test
    client, so data committed in setup is visible inside route handlers.
    """
    flask_app = create_app("testing")

    # Inject StaticPool BEFORE the first DB access (engine is lazy-created
    # in Flask-SQLAlchemy 3.x, so this override takes effect at create_all).
    flask_app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
        "connect_args": {"check_same_thread": False},
        "poolclass": StaticPool,
    }

    with flask_app.app_context():
        _db.create_all()
        yield flask_app
        _db.session.remove()
        _db.drop_all()


@pytest.fixture(scope="function")
def client(app):
    """Flask test client bound to the per-test app."""
    return app.test_client()


# ---------------------------------------------------------------------------
# Pre-built user fixtures
# ---------------------------------------------------------------------------

@pytest.fixture()
def admin_user(app):
    """Persisted admin user: admin@test.local / Admin@12345."""
    return _make_user(
        "admin@test.local",
        "Admin@12345",
        name="Admin User",
        role="admin",
        department="Management",
    )


@pytest.fixture()
def trainer_user(app):
    """Persisted trainer user: trainer@test.local / Trainer@12345."""
    return _make_user(
        "trainer@test.local",
        "Trainer@12345",
        name="Trainer User",
        role="trainer",
        department="HR",
    )


@pytest.fixture()
def employee_user(app):
    """Persisted employee user: employee@test.local / Employee@12345."""
    return _make_user(
        "employee@test.local",
        "Employee@12345",
        name="Employee User",
        role="employee",
        department="Engineering",
    )


# ---------------------------------------------------------------------------
# Seeded data fixtures
# ---------------------------------------------------------------------------

@pytest.fixture()
def seeded_module(app):
    """A TrainingModule with exactly 5 questions; all correct_answer='A'.

    This allows tests to submit all-'A' answers for a perfect score (100),
    or all-'B' answers for score 0.
    """
    mod = TrainingModule(
        title="Test Security Module",
        description="A minimal module used in pytest.",
        content="<p>Test content – trusted HTML.</p>",
        category="security",
        is_active=True,
        order=1,
    )
    _db.session.add(mod)
    _db.session.flush()  # obtain mod.id before adding questions

    for i in range(5):
        q = QuizQuestion(
            module_id=mod.id,
            question=f"Test question {i + 1}: which option is correct?",
            option_a="Correct answer",
            option_b="Wrong option B",
            option_c="Wrong option C",
            option_d="Wrong option D",
            correct_answer="A",
            explanation="Option A is always correct in test fixtures.",
        )
        _db.session.add(q)

    _db.session.commit()
    return mod


@pytest.fixture()
def seeded_campaign(app, admin_user):
    """A PhishingCampaign with is_phishing=True, created by admin_user.

    Correct response: 'phishing'.
    """
    campaign = PhishingCampaign(
        title="Test Phishing Campaign",
        subject="Urgent: Verify Your Account Now",
        sender_name="IT Helpdesk",
        sender_email="helpdesk@fake-domain.net",
        body="Click the link below to avoid account suspension.",
        red_flags="Fake sender domain\nUrgency tactics\nSuspicious link",
        difficulty="easy",
        is_phishing=True,
        created_by=admin_user.id,
    )
    _db.session.add(campaign)
    _db.session.commit()
    return campaign
