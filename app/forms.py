"""WTForms form definitions."""
from flask_wtf import FlaskForm
from wtforms import (
    StringField, PasswordField, TextAreaField, SelectField,
    BooleanField, SubmitField
)
from wtforms.validators import DataRequired, Length, EqualTo, Optional, Regexp


# WTForms' Email validator delegates to the `email_validator` package, which
# rejects special-use TLDs such as the demo accounts' `.local` domain. We use a
# pragmatic format check so internal/lab domains validate while still requiring
# a well-formed address.
Email = lambda: Regexp(  # noqa: E731
    r'^[^@\s]+@[^@\s]+\.[^@\s]+$',
    message='Invalid email address.'
)


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')


class RegistrationForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired(), Length(max=120)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    department = StringField('Department', validators=[Optional(), Length(max=120)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField(
        'Confirm Password',
        validators=[DataRequired(), EqualTo('password', message='Passwords must match.')]
    )
    submit = SubmitField('Create Account')


class CampaignForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=200)])
    subject = StringField('Subject', validators=[DataRequired(), Length(max=255)])
    sender_name = StringField('Sender Name', validators=[DataRequired(), Length(max=120)])
    sender_email = StringField('Sender Email', validators=[DataRequired(), Length(max=120)])
    body = TextAreaField('Email Body', validators=[DataRequired()])
    red_flags = TextAreaField('Red Flags (one per line)', validators=[Optional()])
    difficulty = SelectField(
        'Difficulty',
        choices=[('easy', 'Easy'), ('medium', 'Medium'), ('hard', 'Hard')],
        validators=[DataRequired()]
    )
    is_phishing = BooleanField('This is a phishing email')
    submit = SubmitField('Create Campaign')
