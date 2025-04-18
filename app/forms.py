from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, EmailField, SelectField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo, ValidationError
from app.models import User

class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Log In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(), Length(1, 64),
        Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
               'Username can only contain letters, numbers, dots, or underscores')
    ])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[
        DataRequired(), Length(min=8), 
        EqualTo('password2', message='Passwords must match.')
    ])
    password2 = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(1, 100)])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    subject = StringField('Subject', validators=[DataRequired(), Length(1, 255)])
    message = TextAreaField('Message', validators=[DataRequired()])
    submit = SubmitField('Send Message')

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(1, 255)])
    category = SelectField('Category', coerce=int)
    summary = TextAreaField('Summary', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    published = BooleanField('Published')
    submit = SubmitField('Save')

class ServiceForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(1, 100)])
    short_description = TextAreaField('Short Description', validators=[DataRequired()])
    description = TextAreaField('Full Description', validators=[DataRequired()])
    featured = BooleanField('Featured')
    submit = SubmitField('Save')

class ProjectForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(1, 255)])
    short_description = TextAreaField('Short Description', validators=[DataRequired()])
    description = TextAreaField('Full Description', validators=[DataRequired()])
    client = StringField('Client', validators=[Length(0, 100)])
    technologies_used = TextAreaField('Technologies Used')
    project_url = StringField('Project URL')
    featured = BooleanField('Featured')
    submit = SubmitField('Save')

class AIToolForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(1, 100)])
    description = TextAreaField('Description', validators=[DataRequired()])
    url = StringField('URL', validators=[Length(0, 255)])
    category = StringField('Category', validators=[Length(0, 50)])
    featured = BooleanField('Featured')
    submit = SubmitField('Save')
