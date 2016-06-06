from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField,SelectField,FieldList,FormField,DecimalField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User,Course

class AdminForm(Form):
	pass

class UserForm(Form):
	no = StringField('Number',validators=[Required()])
	username = StringField('Name', validators=[Required()]) 

class AddUserForm(Form):
	users = FieldList(FormField(UserForm),min_entries=5)


class AddCourseForm(Form):
	cname = StringField('Name',validators=[Required()])

