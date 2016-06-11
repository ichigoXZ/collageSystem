from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField,SelectField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User


class LoginForm(Form):
    no = StringField('Number',validators=[Required()])
    password = PasswordField('Password', validators=[Required()])
    select = SelectField('身份', choices=[('Student','Student'), ('Teacher', 'Teacher'),('Administrator','Administrator')])
    remember_me = BooleanField('Keep me logged in')    
    submit = SubmitField('Log In')

class RegistrationForm(Form):
    no = StringField('Number', validators=[Required()])
    password = PasswordField('Password', validators=[
        Required(), EqualTo('password2', message='Passwords must match.')])
    password2 = PasswordField('Confirm password', validators=[Required()])
    tstype = BooleanField('Teacher or not')
    submit = SubmitField('Register')

class ChangePasswordForm(Form):
    old_password = PasswordField('Old password', validators=[Required()])
    password = PasswordField('New password', validators=[
        Required(), EqualTo('password2', message='Passwords must match')])
    password2 = PasswordField('Confirm new password', validators=[Required()])
    submit = SubmitField('Update Password')
