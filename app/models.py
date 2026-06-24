"""Database models for the CyberAware platform."""
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from .extensions import db
from .utils import utcnow


class User(UserMixin, db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, index=True, nullable=False)
    password_hash = db.Column(db.String(255))
    role = db.Column(db.String(20), default='employee', nullable=False)
    department = db.Column(db.String(120))
    created_at = db.Column(db.DateTime, default=utcnow)

    attempts = db.relationship(
        'QuizAttempt', backref='user', lazy=True, cascade='all, delete-orphan'
    )
    progress = db.relationship(
        'UserProgress', backref='user', lazy=True, cascade='all, delete-orphan'
    )
    assignments = db.relationship(
        'PhishingAssignment', backref='user', lazy=True,
        cascade='all, delete-orphan'
    )

    def set_password(self, password):
        self.password_hash = generate_password_hash(password, method='pbkdf2:sha256')

    def check_password(self, password):
        if not self.password_hash:
            return False
        return check_password_hash(self.password_hash, password)

    @property
    def is_admin(self):
        return self.role == 'admin'

    @property
    def is_trainer(self):
        return self.role == 'trainer'

    @property
    def is_employee(self):
        return self.role == 'employee'

    def __repr__(self):
        return f'<User {self.email}>'


class TrainingModule(db.Model):
    __tablename__ = 'training_module'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    content = db.Column(db.Text)  # authored/trusted HTML
    category = db.Column(db.String(100))
    is_active = db.Column(db.Boolean, default=True)
    order = db.Column(db.Integer, default=0)

    questions = db.relationship(
        'QuizQuestion', backref='module', lazy=True,
        cascade='all, delete-orphan'
    )
    progress = db.relationship(
        'UserProgress', backref='module', lazy=True,
        cascade='all, delete-orphan'
    )

    def __repr__(self):
        return f'<TrainingModule {self.title}>'


class QuizQuestion(db.Model):
    __tablename__ = 'quiz_question'

    id = db.Column(db.Integer, primary_key=True)
    module_id = db.Column(db.Integer, db.ForeignKey('training_module.id'), nullable=False)
    question = db.Column(db.Text, nullable=False)
    option_a = db.Column(db.String(500))
    option_b = db.Column(db.String(500))
    option_c = db.Column(db.String(500))
    option_d = db.Column(db.String(500))
    correct_answer = db.Column(db.String(1))  # 'A' | 'B' | 'C' | 'D'
    explanation = db.Column(db.Text)

    def __repr__(self):
        return f'<QuizQuestion {self.id}>'


class QuizAttempt(db.Model):
    __tablename__ = 'quiz_attempt'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    module_id = db.Column(db.Integer, db.ForeignKey('training_module.id'), nullable=False)
    score = db.Column(db.Integer)  # 0-100
    passed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=utcnow)

    module = db.relationship('TrainingModule')

    def __repr__(self):
        return f'<QuizAttempt user={self.user_id} module={self.module_id} score={self.score}>'


class UserProgress(db.Model):
    __tablename__ = 'user_progress'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    module_id = db.Column(db.Integer, db.ForeignKey('training_module.id'), nullable=False)
    status = db.Column(db.String(20), default='not_started')  # not_started|in_progress|completed
    completion_percentage = db.Column(db.Integer, default=0)
    completed_at = db.Column(db.DateTime, nullable=True)

    __table_args__ = (
        db.UniqueConstraint('user_id', 'module_id', name='uq_user_module_progress'),
    )

    def __repr__(self):
        return f'<UserProgress user={self.user_id} module={self.module_id} {self.status}>'


class PhishingCampaign(db.Model):
    __tablename__ = 'phishing_campaign'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    subject = db.Column(db.String(255))
    sender_name = db.Column(db.String(120))
    sender_email = db.Column(db.String(120))
    body = db.Column(db.Text)
    red_flags = db.Column(db.Text)  # newline-separated
    difficulty = db.Column(db.String(20), default='easy')  # easy|medium|hard
    is_phishing = db.Column(db.Boolean, default=True)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_at = db.Column(db.DateTime, default=utcnow)

    assignments = db.relationship(
        'PhishingAssignment', backref='campaign', lazy=True,
        cascade='all, delete-orphan'
    )

    @property
    def correct_response(self):
        return 'phishing' if self.is_phishing else 'legitimate'

    def red_flags_list(self):
        if not self.red_flags:
            return []
        return [line.strip() for line in self.red_flags.splitlines() if line.strip()]

    def __repr__(self):
        return f'<PhishingCampaign {self.title}>'


class PhishingAssignment(db.Model):
    __tablename__ = 'phishing_assignment'

    id = db.Column(db.Integer, primary_key=True)
    campaign_id = db.Column(db.Integer, db.ForeignKey('phishing_campaign.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user_response = db.Column(db.String(20), nullable=True)  # phishing|legitimate
    is_correct = db.Column(db.Boolean, nullable=True)
    responded_at = db.Column(db.DateTime, nullable=True)

    @property
    def responded(self):
        return self.responded_at is not None

    def __repr__(self):
        return f'<PhishingAssignment campaign={self.campaign_id} user={self.user_id}>'


class ActivityLog(db.Model):
    __tablename__ = 'activity_log'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    action = db.Column(db.String(255))
    ip_address = db.Column(db.String(45))
    created_at = db.Column(db.DateTime, default=utcnow)

    user = db.relationship('User')

    def __repr__(self):
        return f'<ActivityLog {self.action}>'
