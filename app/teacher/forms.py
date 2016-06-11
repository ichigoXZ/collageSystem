from flask.ext.wtf import Form
from wtforms import IntegerField,StringField, PasswordField, BooleanField, SubmitField,SelectField,FieldList,FormField,DecimalField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User,Course,Teach,Task,Teach

class taskForm(Form):
	test = SubmitField("add test")
	task = SubmitField('add task')

class gradeForm(Form):
	pass
	
