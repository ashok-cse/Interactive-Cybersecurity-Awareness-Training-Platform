"""
Quiz and training-module tests – CyberAware platform.

Covers:
- Submitting all correct answers produces score=100 and passed=True.
- Submitting all wrong answers produces score=0 and passed=False.
- Partial score: round(correct/total*100), passed if score >= 70 (PASS_THRESHOLD).
- A QuizAttempt record is persisted after every submission.
- UserProgress.status becomes 'completed' (percentage=100, completed_at set)
  when the user passes.
- UserProgress is NOT 'completed' after a failing attempt.

Quiz answer form fields: q_<question_id> = 'A'|'B'|'C'|'D'
seeded_module fixture: 5 questions, all correct_answer='A'.
PASS_THRESHOLD = 70 (from TestingConfig → Config).
"""

import pytest

from app.extensions import db as _db
from app.models import QuizAttempt, QuizQuestion, UserProgress
from tests.conftest import do_login


def _build_quiz_form(questions, answer: str) -> dict:
    """Build POST data for quiz submission: {q_<id>: answer, ...}."""
    return {f"q_{q.id}": answer for q in questions}


class TestQuizScoring:
    """Score calculation and pass/fail logic."""

    def test_all_correct_score_100_passed_true(
        self, client, app, employee_user, seeded_module
    ):
        """All-correct submission: score=100, passed=True."""
        emp_id = employee_user.id
        mod_id = seeded_module.id

        do_login(client, "employee@test.local", "Employee@12345")

        questions = QuizQuestion.query.filter_by(module_id=mod_id).all()
        assert len(questions) == 5, "seeded_module must have exactly 5 questions"

        resp = client.post(
            f"/training/module/{mod_id}/quiz",
            data=_build_quiz_form(questions, "A"),  # 'A' is correct for all
            follow_redirects=False,
        )
        assert resp.status_code == 302, (
            f"Expected 302 redirect after quiz submit, got {resp.status_code}"
        )

        _db.session.expire_all()
        attempt = (
            QuizAttempt.query.filter_by(user_id=emp_id, module_id=mod_id)
            .order_by(QuizAttempt.created_at.desc())
            .first()
        )
        assert attempt is not None, "QuizAttempt was not created"
        assert attempt.score == 100, f"Expected score 100, got {attempt.score}"
        assert attempt.passed is True, "Expected passed=True for perfect score"

    def test_all_wrong_score_0_passed_false(
        self, client, app, employee_user, seeded_module
    ):
        """All-wrong submission: score=0, passed=False."""
        emp_id = employee_user.id
        mod_id = seeded_module.id

        do_login(client, "employee@test.local", "Employee@12345")

        questions = QuizQuestion.query.filter_by(module_id=mod_id).all()
        resp = client.post(
            f"/training/module/{mod_id}/quiz",
            data=_build_quiz_form(questions, "B"),  # 'A' is correct; 'B' is wrong
            follow_redirects=False,
        )
        assert resp.status_code == 302

        _db.session.expire_all()
        attempt = (
            QuizAttempt.query.filter_by(user_id=emp_id, module_id=mod_id)
            .order_by(QuizAttempt.created_at.desc())
            .first()
        )
        assert attempt is not None, "QuizAttempt was not created"
        assert attempt.score == 0, f"Expected score 0, got {attempt.score}"
        assert attempt.passed is False, "Expected passed=False for zero score"

    def test_partial_score_4_of_5_is_80_passed(
        self, client, app, employee_user, seeded_module
    ):
        """4/5 correct → score=round(4/5*100)=80, passed=True (>=70)."""
        emp_id = employee_user.id
        mod_id = seeded_module.id

        do_login(client, "employee@test.local", "Employee@12345")

        questions = (
            QuizQuestion.query.filter_by(module_id=mod_id)
            .order_by(QuizQuestion.id)
            .all()
        )
        assert len(questions) == 5

        form_data = {}
        for idx, q in enumerate(questions):
            form_data[f"q_{q.id}"] = "A" if idx < 4 else "B"  # 4 correct, 1 wrong

        resp = client.post(
            f"/training/module/{mod_id}/quiz",
            data=form_data,
            follow_redirects=False,
        )
        assert resp.status_code == 302

        _db.session.expire_all()
        attempt = (
            QuizAttempt.query.filter_by(user_id=emp_id, module_id=mod_id)
            .order_by(QuizAttempt.created_at.desc())
            .first()
        )
        assert attempt is not None
        assert attempt.score == 80, f"Expected score 80 (4/5*100), got {attempt.score}"
        assert attempt.passed is True, "Expected passed=True for score 80 >= PASS_THRESHOLD 70"

    def test_score_below_threshold_is_failed(
        self, client, app, employee_user, seeded_module
    ):
        """2/5 correct → score=40, passed=False (< 70)."""
        emp_id = employee_user.id
        mod_id = seeded_module.id

        do_login(client, "employee@test.local", "Employee@12345")

        questions = (
            QuizQuestion.query.filter_by(module_id=mod_id)
            .order_by(QuizQuestion.id)
            .all()
        )
        form_data = {}
        for idx, q in enumerate(questions):
            form_data[f"q_{q.id}"] = "A" if idx < 2 else "B"  # 2/5 correct

        resp = client.post(
            f"/training/module/{mod_id}/quiz",
            data=form_data,
            follow_redirects=False,
        )
        assert resp.status_code == 302

        _db.session.expire_all()
        attempt = (
            QuizAttempt.query.filter_by(user_id=emp_id, module_id=mod_id)
            .order_by(QuizAttempt.created_at.desc())
            .first()
        )
        assert attempt is not None
        assert attempt.score == 40, f"Expected score 40 (2/5*100), got {attempt.score}"
        assert attempt.passed is False, "Expected passed=False for score 40 < 70"


class TestQuizAttemptPersistence:
    """QuizAttempt is written to the database on every submission."""

    def test_attempt_record_created_after_submission(
        self, client, app, employee_user, seeded_module
    ):
        """A QuizAttempt row exists for the user+module after submitting."""
        emp_id = employee_user.id
        mod_id = seeded_module.id

        initial_count = QuizAttempt.query.filter_by(user_id=emp_id).count()
        do_login(client, "employee@test.local", "Employee@12345")

        questions = QuizQuestion.query.filter_by(module_id=mod_id).all()
        client.post(
            f"/training/module/{mod_id}/quiz",
            data=_build_quiz_form(questions, "A"),
            follow_redirects=False,
        )

        _db.session.expire_all()
        final_count = QuizAttempt.query.filter_by(user_id=emp_id).count()
        assert final_count == initial_count + 1, (
            f"Expected 1 new QuizAttempt (went from {initial_count} to {final_count})"
        )

    def test_multiple_attempts_all_persisted(
        self, client, app, employee_user, seeded_module
    ):
        """Each quiz submission (even repeated) creates a separate QuizAttempt."""
        emp_id = employee_user.id
        mod_id = seeded_module.id

        do_login(client, "employee@test.local", "Employee@12345")
        questions = QuizQuestion.query.filter_by(module_id=mod_id).all()

        for _ in range(3):
            client.post(
                f"/training/module/{mod_id}/quiz",
                data=_build_quiz_form(questions, "A"),
                follow_redirects=False,
            )

        _db.session.expire_all()
        count = QuizAttempt.query.filter_by(user_id=emp_id, module_id=mod_id).count()
        assert count == 3, f"Expected 3 QuizAttempt records after 3 submissions, got {count}"


class TestModuleProgress:
    """UserProgress reflects quiz outcomes correctly."""

    def test_progress_completed_after_passing_quiz(
        self, client, app, employee_user, seeded_module
    ):
        """Passing quiz → UserProgress.status='completed', percentage=100, completed_at set."""
        emp_id = employee_user.id
        mod_id = seeded_module.id

        do_login(client, "employee@test.local", "Employee@12345")
        questions = QuizQuestion.query.filter_by(module_id=mod_id).all()
        client.post(
            f"/training/module/{mod_id}/quiz",
            data=_build_quiz_form(questions, "A"),
            follow_redirects=False,
        )

        _db.session.expire_all()
        progress = UserProgress.query.filter_by(
            user_id=emp_id, module_id=mod_id
        ).first()
        assert progress is not None, "UserProgress record not created after quiz pass"
        assert progress.status == "completed", (
            f"Expected status 'completed', got '{progress.status}'"
        )
        assert progress.completion_percentage == 100, (
            f"Expected percentage 100, got {progress.completion_percentage}"
        )
        assert progress.completed_at is not None, "completed_at should be set after passing"

    def test_progress_not_completed_after_failing_quiz(
        self, client, app, employee_user, seeded_module
    ):
        """Failing quiz → UserProgress must NOT be 'completed'."""
        emp_id = employee_user.id
        mod_id = seeded_module.id

        do_login(client, "employee@test.local", "Employee@12345")
        questions = QuizQuestion.query.filter_by(module_id=mod_id).all()
        client.post(
            f"/training/module/{mod_id}/quiz",
            data=_build_quiz_form(questions, "B"),  # all wrong → score 0
            follow_redirects=False,
        )

        _db.session.expire_all()
        progress = UserProgress.query.filter_by(
            user_id=emp_id, module_id=mod_id
        ).first()
        if progress is not None:
            assert progress.status != "completed", (
                "UserProgress must not be 'completed' after a failed quiz attempt"
            )
            assert progress.completed_at is None, (
                "completed_at must be None after a failed attempt"
            )
