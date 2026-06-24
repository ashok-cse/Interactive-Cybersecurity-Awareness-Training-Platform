"""
Admin and staff route tests – CyberAware platform.

Covers:
- Admin can list users at GET /admin/users (200).
- Trainer (staff) can access GET /admin/analytics (200).
- Phishing assignment response is logged correctly:
  - user_response, responded_at, and is_correct are stored.
  - is_correct=True when user correctly identifies a phishing email.
  - is_correct=False when user incorrectly labels a phishing email as legitimate.
- CSV report endpoints return 200 with Content-Type: text/csv.

Phishing grading rule (from contract):
  correct_response = 'phishing' if campaign.is_phishing else 'legitimate'
  is_correct = (user_response == correct_response)
"""

import pytest

from app.extensions import db as _db
from app.models import PhishingAssignment, PhishingCampaign, User
from tests.conftest import _make_user, do_login


# ---------------------------------------------------------------------------
# Admin user management
# ---------------------------------------------------------------------------

class TestAdminUsersList:
    """GET /admin/users — admin-only route."""

    def test_admin_can_list_users(self, client, admin_user):
        """Admin receives HTTP 200 from GET /admin/users."""
        do_login(client, "admin@test.local", "Admin@12345")
        resp = client.get("/admin/users")
        assert resp.status_code == 200, (
            f"Admin expected 200 on /admin/users, got {resp.status_code}"
        )

    def test_trainer_cannot_access_admin_users(self, client, trainer_user):
        """Trainer (staff) must be denied access to the admin-only /admin/users."""
        do_login(client, "trainer@test.local", "Trainer@12345")
        resp = client.get("/admin/users", follow_redirects=False)
        assert resp.status_code in (302, 403), (
            f"Trainer should not access /admin/users; got {resp.status_code}"
        )

    def test_employee_cannot_access_admin_users(self, client, employee_user):
        """Employee role must be denied /admin/users."""
        do_login(client, "employee@test.local", "Employee@12345")
        resp = client.get("/admin/users", follow_redirects=False)
        assert resp.status_code in (302, 403)


# ---------------------------------------------------------------------------
# Analytics (staff: admin + trainer)
# ---------------------------------------------------------------------------

class TestStaffAnalytics:
    """GET /admin/analytics — staff route (admin or trainer)."""

    def test_trainer_can_access_analytics(self, client, trainer_user):
        """Trainer receives HTTP 200 from GET /admin/analytics."""
        do_login(client, "trainer@test.local", "Trainer@12345")
        resp = client.get("/admin/analytics")
        assert resp.status_code == 200, (
            f"Trainer expected 200 on /admin/analytics, got {resp.status_code}"
        )

    def test_admin_can_access_analytics(self, client, admin_user):
        """Admin receives HTTP 200 from GET /admin/analytics."""
        do_login(client, "admin@test.local", "Admin@12345")
        resp = client.get("/admin/analytics")
        assert resp.status_code == 200


# ---------------------------------------------------------------------------
# Phishing assignment response logging
# ---------------------------------------------------------------------------

class TestPhishingAssignmentResponse:
    """POST /phishing/email/<id>/respond — grading and persistence."""

    def _create_assignment(self, campaign_id: int, user_id: int) -> int:
        """Helper: create a PhishingAssignment and return its id."""
        assignment = PhishingAssignment(
            campaign_id=campaign_id,
            user_id=user_id,
        )
        _db.session.add(assignment)
        _db.session.commit()
        return assignment.id

    def test_correct_phishing_response_is_recorded(
        self, client, app, employee_user, seeded_campaign
    ):
        """User responds 'phishing' to a phishing email → is_correct=True, responded_at set."""
        emp_id = employee_user.id
        assignment_id = self._create_assignment(seeded_campaign.id, emp_id)

        do_login(client, "employee@test.local", "Employee@12345")
        resp = client.post(
            f"/phishing/email/{assignment_id}/respond",
            data={"response": "phishing"},
            follow_redirects=False,
        )
        assert resp.status_code in (302, 200), (
            f"Unexpected status {resp.status_code} for phishing respond"
        )

        _db.session.expire_all()
        updated = _db.session.get(PhishingAssignment, assignment_id)
        assert updated is not None
        assert updated.user_response == "phishing", (
            f"Expected user_response='phishing', got {updated.user_response!r}"
        )
        assert updated.is_correct is True, (
            "Expected is_correct=True: 'phishing' is the correct response for is_phishing=True"
        )
        assert updated.responded_at is not None, (
            "responded_at must be set after the user responds"
        )

    def test_incorrect_phishing_response_is_recorded(
        self, client, app, employee_user, seeded_campaign
    ):
        """User responds 'legitimate' to a phishing email → is_correct=False."""
        emp_id = employee_user.id
        assignment_id = self._create_assignment(seeded_campaign.id, emp_id)

        do_login(client, "employee@test.local", "Employee@12345")
        resp = client.post(
            f"/phishing/email/{assignment_id}/respond",
            data={"response": "legitimate"},
            follow_redirects=False,
        )
        assert resp.status_code in (302, 200)

        _db.session.expire_all()
        updated = _db.session.get(PhishingAssignment, assignment_id)
        assert updated is not None
        assert updated.user_response == "legitimate"
        assert updated.is_correct is False, (
            "Expected is_correct=False: 'legitimate' is wrong for is_phishing=True"
        )
        assert updated.responded_at is not None

    def test_legitimate_email_correct_response_is_legitimate(
        self, client, app, employee_user, admin_user
    ):
        """User correctly identifies a legitimate (non-phishing) email → is_correct=True."""
        # Create a campaign that is NOT a phishing email
        legit_campaign = PhishingCampaign(
            title="Legitimate Newsletter",
            subject="Monthly Security Update",
            sender_name="Security Team",
            sender_email="security@company.com",
            body="Here is your monthly security newsletter.",
            red_flags="",
            difficulty="hard",
            is_phishing=False,  # legitimate email
            created_by=admin_user.id,
        )
        _db.session.add(legit_campaign)
        _db.session.commit()

        assignment_id = self._create_assignment(legit_campaign.id, employee_user.id)

        do_login(client, "employee@test.local", "Employee@12345")
        resp = client.post(
            f"/phishing/email/{assignment_id}/respond",
            data={"response": "legitimate"},  # correct response for non-phishing
            follow_redirects=False,
        )
        assert resp.status_code in (302, 200)

        _db.session.expire_all()
        updated = _db.session.get(PhishingAssignment, assignment_id)
        assert updated is not None
        assert updated.is_correct is True, (
            "Expected is_correct=True: 'legitimate' is correct for is_phishing=False"
        )


# ---------------------------------------------------------------------------
# CSV report endpoints
# ---------------------------------------------------------------------------

class TestCSVReports:
    """GET /reports/*.csv — staff routes returning downloadable CSVs."""

    def test_user_progress_csv_status_200(self, client, admin_user):
        """GET /reports/user-progress.csv returns 200."""
        do_login(client, "admin@test.local", "Admin@12345")
        resp = client.get("/reports/user-progress.csv")
        assert resp.status_code == 200, (
            f"Expected 200 for user-progress CSV, got {resp.status_code}"
        )

    def test_user_progress_csv_content_type(self, client, admin_user):
        """GET /reports/user-progress.csv Content-Type must contain text/csv."""
        do_login(client, "admin@test.local", "Admin@12345")
        resp = client.get("/reports/user-progress.csv")
        if resp.status_code == 200:
            content_type = resp.headers.get("Content-Type", "")
            assert "text/csv" in content_type, (
                f"Expected text/csv content-type, got: {content_type!r}"
            )

    def test_quiz_scores_csv_status_200(self, client, admin_user):
        """GET /reports/quiz-scores.csv returns 200."""
        do_login(client, "admin@test.local", "Admin@12345")
        resp = client.get("/reports/quiz-scores.csv")
        assert resp.status_code == 200, (
            f"Expected 200 for quiz-scores CSV, got {resp.status_code}"
        )

    def test_quiz_scores_csv_content_type(self, client, admin_user):
        """GET /reports/quiz-scores.csv Content-Type must contain text/csv."""
        do_login(client, "admin@test.local", "Admin@12345")
        resp = client.get("/reports/quiz-scores.csv")
        if resp.status_code == 200:
            assert "text/csv" in resp.headers.get("Content-Type", "")

    def test_phishing_csv_status_200(self, client, admin_user):
        """GET /reports/phishing.csv returns 200."""
        do_login(client, "admin@test.local", "Admin@12345")
        resp = client.get("/reports/phishing.csv")
        assert resp.status_code == 200, (
            f"Expected 200 for phishing CSV, got {resp.status_code}"
        )

    def test_phishing_csv_content_type(self, client, admin_user):
        """GET /reports/phishing.csv Content-Type must contain text/csv."""
        do_login(client, "admin@test.local", "Admin@12345")
        resp = client.get("/reports/phishing.csv")
        if resp.status_code == 200:
            assert "text/csv" in resp.headers.get("Content-Type", "")

    def test_csv_employee_access_denied(self, client, employee_user):
        """Employee must not download CSV reports (403 or redirect)."""
        do_login(client, "employee@test.local", "Employee@12345")
        for endpoint in (
            "/reports/user-progress.csv",
            "/reports/quiz-scores.csv",
            "/reports/phishing.csv",
        ):
            resp = client.get(endpoint, follow_redirects=False)
            assert resp.status_code in (302, 403), (
                f"Employee accessed {endpoint!r} with status {resp.status_code}"
            )
