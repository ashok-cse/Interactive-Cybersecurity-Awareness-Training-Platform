"""
Security tests – CyberAware platform.

Covers:
- Role-based access control: employee cannot reach admin-only routes.
- Anonymous users are redirected to /login on every protected route.
- SQL injection strings in the login email field cause no 500 error and no
  authentication bypass.
- XSS payloads submitted in user-supplied fields are HTML-escaped in rendered
  output (raw <script> tag never appears in the response body).
- Security headers (X-Frame-Options, X-Content-Type-Options, CSP) are present
  on every response.
"""

import pytest

from app.extensions import db as _db
from app.models import User
from tests.conftest import _make_user, do_login


# ---------------------------------------------------------------------------
# Role-based access control
# ---------------------------------------------------------------------------

class TestAccessControl:
    """Verify that role boundaries are enforced on admin/staff routes."""

    def test_employee_cannot_access_admin_users_page(self, client, employee_user):
        """GET /admin/users as an employee must return 403 or redirect away."""
        do_login(client, "employee@test.local", "Employee@12345")
        resp = client.get("/admin/users", follow_redirects=False)
        assert resp.status_code in (302, 403), (
            f"/admin/users returned {resp.status_code} for employee role — "
            "expected 403 or redirect"
        )
        if resp.status_code == 302:
            location = resp.headers.get("Location", "")
            # Must not be redirected further into the admin area
            assert "users" not in location.lower() or "admin" not in location.lower()

    def test_employee_cannot_access_admin_analytics(self, client, employee_user):
        """GET /admin/analytics as an employee must return 403 or redirect."""
        do_login(client, "employee@test.local", "Employee@12345")
        resp = client.get("/admin/analytics", follow_redirects=False)
        assert resp.status_code in (302, 403), (
            f"Employee accessed /admin/analytics with status {resp.status_code}"
        )

    def test_employee_cannot_access_csv_reports(self, client, employee_user):
        """GET /reports/user-progress.csv as employee must be denied."""
        do_login(client, "employee@test.local", "Employee@12345")
        resp = client.get("/reports/user-progress.csv", follow_redirects=False)
        assert resp.status_code in (302, 403), (
            f"Employee accessed CSV report with status {resp.status_code}"
        )


# ---------------------------------------------------------------------------
# Anonymous / unauthenticated access
# ---------------------------------------------------------------------------

class TestAnonymousRedirects:
    """Unauthenticated requests to protected routes must redirect to /login."""

    PROTECTED_ROUTES = [
        "/dashboard",
        "/profile",
        "/training/",
        "/phishing/",
        "/admin/users",
        "/admin/analytics",
    ]

    @pytest.mark.parametrize("route", PROTECTED_ROUTES)
    def test_anonymous_redirected_to_login(self, client, route):
        """Anonymous GET on a protected route must return 302 or 401."""
        resp = client.get(route, follow_redirects=False)
        assert resp.status_code in (302, 401), (
            f"Anonymous access to {route!r} returned {resp.status_code} "
            "(expected 302 redirect to /login or 401)"
        )
        if resp.status_code == 302:
            location = resp.headers.get("Location", "")
            assert "login" in location.lower(), (
                f"Redirect from {route!r} does not go to /login: {location!r}"
            )


# ---------------------------------------------------------------------------
# SQL injection prevention
# ---------------------------------------------------------------------------

class TestSQLInjection:
    """SQL injection strings in form fields must be handled safely by the ORM."""

    SQL_PAYLOADS = [
        "' OR '1'='1",
        "admin'--",
        "'; DROP TABLE user;--",
        "' UNION SELECT id,email,password_hash FROM user--",
        "\" OR \"1\"=\"1",
    ]

    @pytest.mark.parametrize("payload", SQL_PAYLOADS)
    def test_sql_injection_in_email_no_500(self, client, payload):
        """SQL injection in the email field must not trigger a 500 error."""
        resp = client.post(
            "/login",
            data={"email": payload, "password": "anything"},
            follow_redirects=True,
        )
        assert resp.status_code != 500, (
            f"Server error (500) on SQL injection payload: {payload!r}"
        )

    @pytest.mark.parametrize("payload", SQL_PAYLOADS)
    def test_sql_injection_in_email_no_auth_bypass(self, client, payload):
        """SQL injection in the email field must not bypass authentication."""
        resp = client.post(
            "/login",
            data={"email": payload, "password": "anything"},
            follow_redirects=False,
        )
        if resp.status_code == 302:
            location = resp.headers.get("Location", "")
            assert "dashboard" not in location.lower(), (
                f"SQL injection payload {payload!r} bypassed authentication!"
            )

    def test_injection_with_valid_email_prefix_no_bypass(self, client, employee_user):
        """An injection appended to a real email must not authenticate."""
        malicious = "employee@test.local' OR '1'='1"
        resp = client.post(
            "/login",
            data={"email": malicious, "password": "wrongpassword"},
            follow_redirects=False,
        )
        if resp.status_code == 302:
            location = resp.headers.get("Location", "")
            assert "dashboard" not in location.lower(), (
                "Auth bypass via email-prefix injection!"
            )


# ---------------------------------------------------------------------------
# XSS prevention
# ---------------------------------------------------------------------------

class TestXSSPrevention:
    """User-supplied data must be HTML-escaped in rendered responses."""

    XSS_SCRIPT = "<script>alert('xss')</script>"
    XSS_BYTES = b"<script>alert('xss')</script>"

    def test_xss_in_registration_name_is_escaped(self, client, app):
        """A <script> tag in the 'name' registration field must be escaped."""
        resp = client.post(
            "/register",
            data={
                "name": self.XSS_SCRIPT,
                "email": "xss1@example.com",
                "department": "Test",
                "password": "Securepass1!",
                "confirm_password": "Securepass1!",
            },
            follow_redirects=True,
        )
        assert self.XSS_BYTES not in resp.data, (
            "Raw <script> tag found unescaped in POST /register response!"
        )

    def test_xss_in_name_escaped_on_profile_page(self, client, app):
        """The profile page must escape a user's name that contains a <script> tag."""
        _make_user(
            "xss2@example.com",
            "Securepass1!",
            name=self.XSS_SCRIPT,
            role="employee",
        )
        login_resp = do_login(client, "xss2@example.com", "Securepass1!")
        if login_resp.status_code != 302:
            pytest.skip("Login failed; profile page test cannot proceed")

        resp = client.get("/profile", follow_redirects=True)
        assert self.XSS_BYTES not in resp.data, (
            "Raw <script> tag found unescaped on /profile page!"
        )

    def test_xss_in_name_escaped_on_dashboard(self, client, app):
        """The dashboard must escape a user name containing a <script> tag."""
        _make_user(
            "xss3@example.com",
            "Securepass1!",
            name=self.XSS_SCRIPT,
            role="employee",
        )
        login_resp = do_login(client, "xss3@example.com", "Securepass1!")
        if login_resp.status_code != 302:
            pytest.skip("Login failed; dashboard test cannot proceed")

        resp = client.get("/dashboard", follow_redirects=True)
        assert self.XSS_BYTES not in resp.data, (
            "Raw <script> tag found unescaped on /dashboard!"
        )


# ---------------------------------------------------------------------------
# Security headers
# ---------------------------------------------------------------------------

class TestSecurityHeaders:
    """HTTP security headers must be present on every response (after_request hook)."""

    def test_x_frame_options_deny(self, client):
        """X-Frame-Options header must be present and set to DENY."""
        resp = client.get("/")
        assert "X-Frame-Options" in resp.headers, (
            "X-Frame-Options header is missing from the response"
        )
        assert resp.headers["X-Frame-Options"].upper() == "DENY", (
            f"X-Frame-Options should be DENY, got: {resp.headers['X-Frame-Options']!r}"
        )

    def test_x_content_type_options_nosniff(self, client):
        """X-Content-Type-Options header must be present and set to nosniff."""
        resp = client.get("/")
        assert "X-Content-Type-Options" in resp.headers, (
            "X-Content-Type-Options header is missing"
        )
        assert resp.headers["X-Content-Type-Options"].lower() == "nosniff", (
            f"Expected 'nosniff', got: {resp.headers['X-Content-Type-Options']!r}"
        )

    def test_content_security_policy_present(self, client):
        """Content-Security-Policy header must be present."""
        resp = client.get("/")
        assert "Content-Security-Policy" in resp.headers, (
            "Content-Security-Policy header is missing"
        )

    def test_referrer_policy_present(self, client):
        """Referrer-Policy header must be present."""
        resp = client.get("/")
        assert "Referrer-Policy" in resp.headers, (
            "Referrer-Policy header is missing"
        )

    def test_headers_present_on_authenticated_route(self, client, employee_user):
        """Security headers must also be returned on authenticated routes."""
        do_login(client, "employee@test.local", "Employee@12345")
        resp = client.get("/dashboard", follow_redirects=True)
        assert "X-Frame-Options" in resp.headers
        assert "X-Content-Type-Options" in resp.headers
