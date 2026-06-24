"""Tests for the demo seed data (seed.py).

Each test runs against the function-scoped in-memory DB from the ``app``
fixture, so calling ``seed()`` here is isolated and does not affect other tests.
"""
import pytest

from seed import seed
from app.models import User, TrainingModule, QuizQuestion, PhishingCampaign


NEW_MODULE_TITLES = [
    "Password & Authentication Attacks",
    "Malware & Ransomware",
    "Network & Web Attacks",
]


@pytest.fixture()
def seeded(app):
    """Populate the fresh in-memory DB with the demo seed data."""
    seed()  # detects the active app context and seeds in-place
    return app


class TestSeedCounts:
    def test_expected_record_counts(self, seeded):
        # 21 modules (6 existing + 15 top-attack), every quiz 30 questions.
        assert User.query.count() == 5
        assert TrainingModule.query.count() == 21
        assert QuizQuestion.query.count() == 21 * 30
        assert PhishingCampaign.query.count() == 6

    def test_seed_is_idempotent(self, seeded):
        # Running again must not duplicate data (skips when admin exists).
        seed()
        assert User.query.count() == 5
        assert TrainingModule.query.count() == 21
        assert QuizQuestion.query.count() == 21 * 30


class TestSeedContent:
    def test_demo_accounts_exist_with_roles(self, seeded):
        roles = {
            "admin@cyberaware.local": "admin",
            "trainer@cyberaware.local": "trainer",
            "employee@cyberaware.local": "employee",
        }
        for email, role in roles.items():
            user = User.query.filter_by(email=email).first()
            assert user is not None, f"missing demo account {email}"
            assert user.role == role

    def test_demo_passwords_are_hashed_not_plaintext(self, seeded):
        admin = User.query.filter_by(email="admin@cyberaware.local").first()
        assert admin.password_hash != "Admin@12345"
        assert admin.password_hash.startswith("pbkdf2:")
        assert admin.check_password("Admin@12345")

    def test_new_attack_modules_present(self, seeded):
        titles = {m.title for m in TrainingModule.query.all()}
        for expected in NEW_MODULE_TITLES:
            assert expected in titles, f"missing module: {expected}"

    def test_every_module_has_at_least_five_questions(self, seeded):
        for module in TrainingModule.query.all():
            count = QuizQuestion.query.filter_by(module_id=module.id).count()
            assert count >= 5, f"{module.title} has only {count} questions"

    def test_every_question_has_valid_correct_answer(self, seeded):
        for q in QuizQuestion.query.all():
            assert q.correct_answer in {"A", "B", "C", "D"}
            assert q.explanation, f"question {q.id} missing explanation"

    def test_campaigns_include_phishing_and_legitimate(self, seeded):
        phishing = PhishingCampaign.query.filter_by(is_phishing=True).count()
        legit = PhishingCampaign.query.filter_by(is_phishing=False).count()
        assert phishing >= 1
        assert legit >= 1
