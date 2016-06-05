from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..models import Student


class LoginForm(Form):
    sno = StringField('sno',validators=[Required()])
    password = PasswordField('Password', validators=[Required()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')

class RegistrationForm(Form):
    sno = StringField('sno', validators=[Required()])
    password = PasswordField('Password', validators=[
        Required(), EqualTo('password2', message='Passwords must match.')])
    password2 = PasswordField('Confirm password', validators=[Required()])
    submit = SubmitField('Register')

    def validate_sno(self, field):
        if Student.query.filter_by(sno=field.data).first():
        	if Student.query.filter_by(sno=field.data).first().password_hash:
        		raise ValidationError('Student already registered.')
        else:
        	raise ValidationError('No such student in collage.')

