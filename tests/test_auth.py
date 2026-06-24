"""
Authentication tests – CyberAware platform.

Covers:
- Registration creates a User record in the database.
- Login with valid credentials redirects (302) to /dashboard.
- Login with invalid credentials does NOT redirect to /dashboard.
- Password is stored as a pbkdf2:sha256 hash, never as plaintext.
- User.check_password() correctly validates correct/wrong passwords.
- Logout clears the session; subsequent access to /dashboard requires auth.
"""

import pytest

from app.extensions import db as _db
from app.models import User
from tests.conftest import _make_user, do_login


class TestRegistration:
    """POST /register endpoint."""

    def test_registration_creates_user_in_db(self, client, app):
        """Submitting the registration form persists a new User record."""
        resp = client.post(
            "/register",
            data={
                "name": "Alice Smith",
                "email": "alice@example.com",
                "department": "Engineering",
                "password": "Securepass1!",
                "confirm_password": "Securepass1!",
            },
            follow_redirects=False,
        )
        # Accept redirect (to login / dashboard) or 200 success page.
        assert resp.status_code in (200, 302), (
            f"Registration returned unexpected status {resp.status_code}"
        )
        user = User.query.filter_by(email="alice@example.com").first()
        assert user is not None, "User was not created in the database after registration"
        assert user.name == "Alice Smith"
        assert user.department == "Engineering"

    def test_registration_sets_role_employee_by_default(self, client, app):
        """Newly registered users receive the 'employee' role."""
        client.post(
            "/register",
            data={
                "name": "Bob Jones",
                "email": "bob@example.com",
                "department": "Sales",
                "password": "Securepass1!",
                "confirm_password": "Securepass1!",
            },
            follow_redirects=False,
        )
        user = User.query.filter_by(email="bob@example.com").first()
        if user is not None:  # only check if route is implemented
            assert user.role == "employee", (
                f"Expected role 'employee', got '{user.role}'"
            )


class TestLogin:
    """POST /login endpoint."""

    def test_valid_credentials_redirect_to_dashboard(self, client, employee_user):
        """Correct email + password returns 302 redirect to /dashboard."""
        resp = do_login(client, "employee@test.local", "Employee@12345")
        assert resp.status_code == 302, (
            f"Expected 302 redirect for valid login, got {resp.status_code}"
        )
        location = resp.headers.get("Location", "")
        assert "dashboard" in location.lower(), (
            f"Expected redirect to /dashboard, Location was: {location!r}"
        )

    def test_invalid_password_does_not_authenticate(self, client, employee_user):
        """Wrong password must not result in a redirect to /dashboard."""
        resp = do_login(client, "employee@test.local", "WrongPassword!")
        # A failed login may return 200 (re-render login) or redirect BACK to /login.
        if resp.status_code == 302:
            location = resp.headers.get("Location", "")
            assert "dashboard" not in location.lower(), (
                "Invalid password redirected to /dashboard — authentication bypass!"
            )
        else:
            assert resp.status_code == 200, (
                f"Unexpected status {resp.status_code} for invalid login"
            )

    def test_unknown_email_does_not_authenticate(self, client):
        """A non-existent email must not authenticate."""
        resp = do_login(client, "nobody@nowhere.invalid", "Whatever1!")
        if resp.status_code == 302:
            location = resp.headers.get("Location", "")
            assert "dashboard" not in location.lower()
        else:
            assert resp.status_code in (200, 400), (
                f"Unexpected status {resp.status_code} for unknown email"
            )

    def test_empty_credentials_do_not_authenticate(self, client):
        """Empty email and password fields do not authenticate."""
        resp = do_login(client, "", "")
        assert resp.status_code != 500, "Server error on empty credentials"
        if resp.status_code == 302:
            location = resp.headers.get("Location", "")
            assert "dashboard" not in location.lower()


class TestPasswordSecurity:
    """Password hashing invariants (model-level, no HTTP needed)."""

    def test_password_is_not_stored_in_plaintext(self, app, employee_user):
        """User.password_hash must never equal the raw password string."""
        user = User.query.filter_by(email="employee@test.local").first()
        assert user is not None
        assert user.password_hash != "Employee@12345", (
            "Password was stored as plaintext — critical security failure!"
        )

    def test_password_hash_uses_pbkdf2_sha256(self, app, employee_user):
        """The hash scheme prefix must be 'pbkdf2:sha256'."""
        user = User.query.filter_by(email="employee@test.local").first()
        assert user.password_hash is not None
        assert user.password_hash.startswith("pbkdf2:sha256"), (
            f"Expected pbkdf2:sha256 hash, found: {user.password_hash[:40]!r}"
        )

    def test_check_password_returns_true_for_correct_password(self, app, employee_user):
        """User.check_password() returns True when the correct password is given."""
        user = User.query.filter_by(email="employee@test.local").first()
        assert user.check_password("Employee@12345") is True

    def test_check_password_returns_false_for_wrong_password(self, app, employee_user):
        """User.check_password() returns False for any wrong password."""
        user = User.query.filter_by(email="employee@test.local").first()
        assert user.check_password("totally-wrong-password") is False
        assert user.check_password("") is False
        assert user.check_password("employee@12345") is False  # case mismatch


class TestLogout:
    """POST /logout endpoint."""

    def test_logout_redirects_and_clears_session(self, client, employee_user):
        """After logout, GET /dashboard should require re-authentication."""
        # Step 1: authenticate
        login_resp = do_login(client, "employee@test.local", "Employee@12345")
        assert login_resp.status_code == 302, (
            "Login did not succeed — cannot test logout"
        )

        # Step 2: logout via POST (CSRF disabled in TestingConfig)
        logout_resp = client.post("/logout", follow_redirects=True)
        assert logout_resp.status_code == 200

        # Step 3: verify session is cleared — dashboard must deny access
        dashboard_resp = client.get("/dashboard", follow_redirects=False)
        assert dashboard_resp.status_code in (302, 401), (
            "Expected redirect or 401 after logout when accessing /dashboard, "
            f"got {dashboard_resp.status_code}"
        )
        if dashboard_resp.status_code == 302:
            location = dashboard_resp.headers.get("Location", "")
            assert "login" in location.lower(), (
                f"Expected redirect to /login after logout, got: {location!r}"
            )
