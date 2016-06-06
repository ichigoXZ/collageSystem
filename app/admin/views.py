from flask import render_template, redirect, request, url_for, flash
from . import admin
from .. import db
from ..models import User,Course,Teach
from .forms import AdminForm,AddUserForm,UserForm

@admin.route('/',methods=['GET','POST'])
def index():
	#form = AdminForm()
	studentsform = AddUserForm()
	teachersform = AddUserForm()
	students = User.query.filter_by(permission=2).all()
	teachers = User.query.filter_by(permission=1).all()
	while len(studentsform.users) > 0:
		studentsform.users.pop_entry()

	for student in students:
		studentform = UserForm()
		studentform.no = student.no
		studentform.username = student.name
		studentsform.users.append_entry(studentform)
	
	if 'addstu' in request.form and request.method == 'POST':
		stu = User(no=request.form['sno'],name=request.form['sname'],permission=2)
		db.session.add(stu)
		db.session.commit()
		#return render_template('admin/admin.html',studentsform=studentsform,teachersform=teachersform)
		return redirect(request.args.get('next') or url_for('admin.index'))

	while len(teachersform.users) > 0:
		teachersform.users.pop_entry()

	for teacher in teachers:
		teacherform = UserForm()
		teacherform.username = teacher.name
		teacherform.no = teacher.no
		teachersform.users.append_entry(teacherform)	

	if 'addtea' in request.form and request.method == 'POST':
		tea = User(no=request.form['tno'],name=request.form['tname'],permission=1)
		db.session.add(tea)
		db.session.commit()
		return redirect(request.args.get('next') or url_for('admin.index'))

	return render_template('admin/admin.html',studentsform=studentsform,teachersform=teachersform)

@admin.route('/modify/<value>',methods=['GET','POST'])
def modify(value):
	flash("came")
	return render_template('admin/admin.html',studentsform=studentsform,teachersform=teachersform)
