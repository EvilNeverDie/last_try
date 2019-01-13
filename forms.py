from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length


class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=150)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=50)])
    remember_me = BooleanField('remember me')


class RegistrationForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid Email'), Length(max=100)])
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=150)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=50)])


class UrlForm(FlaskForm):
    Url = StringField('url', validators=[InputRequired(), Length(max=500)])
