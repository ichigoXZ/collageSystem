from flask.ext.wtf import Form
from wtforms import IntegerField,StringField, PasswordField, BooleanField, SubmitField,SelectField,FieldList,FormField,DecimalField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User,Course

class AdminForm(Form):
	pass

class UserForm(Form):
	uid = IntegerField("id")
	no = StringField('Number',validators=[Required()])
	username = StringField('Name', validators=[Required()]) 

class AddUserForm(Form):
	users = FieldList(FormField(UserForm),min_entries=5)
	submit = SubmitField("Update", validators=[Required()])

class AddCourseForm(Form):
	cname = StringField('Name',validators=[Required()])
	credithour = DecimalField('credithour',places=2,validators=[Required()])
	submit = SubmitField("AddCourse",validators=[Required()])

class AddTeachForm(Form):
	tno = StringField("Teacher Number",validators=[Required()])
	cname = StringField("Course Name",validators=[Required()])
	submit = SubmitField('Add a teacher to course',validators=[Required()])