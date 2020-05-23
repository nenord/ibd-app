from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, EqualTo, Email, ValidationError, Length
from app.models import User

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    repeat_password = PasswordField('Repeat Password', validators=[DataRequired(),
        EqualTo('password', message='Passwords must match')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username = username.data).first()
        if user is not None:
            raise ValidationError('Choose a different userename!')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Choose a different email!')

class SearchRestForm(FlaskForm):
    location = StringField('Location *', validators=[DataRequired()], render_kw = {'placeholder': 'Town or city'})
    term = StringField('Additional search term - optional', render_kw = {'placeholder': 'Restaurant name, type or a street'})
    submit = SubmitField('Search')

class SearchPostsForm(FlaskForm):
    location = StringField('Location *', validators=[DataRequired()], render_kw = {'placeholder': 'Town or city'})
    submit = SubmitField('Search')
