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

    '''
    def validate_no(self, field):
      stu = Student.query.filter_by(sno=field.data).first()
      if stu:
        if stu.password_hash:
          raise ValidationError('This Student has already registered.')
        else:
          tea = Teacher.query.filter_by(tno=field.data).first()
          if tea:
            if tea.password_hash:
              raise ValidationError('This teacher has already registered.')
          else:
            raise ValidationError('No such people in collage.')
    '''
