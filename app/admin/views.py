from flask import render_template, redirect, request, url_for, flash
from . import admin
from .. import db
from ..models import User,Course,Teach
from .forms import AdminForm,AddUserForm,UserForm,AddCourseForm,AddTeachForm

@admin.route('/',methods=['GET','POST'])
def index():
	students = User.query.filter_by(permission=2).all()
	teachers = User.query.filter_by(permission=1).all()
	courses = Course.query.all()
	teaching = Teach.query.all()

	addcourseform = AddCourseForm()	
	if addcourseform.validate_on_submit():
		c = Course(cname=addcourseform.cname.data,credithour=addcourseform.credithour.data)
		db.session.add(c)
		db.session.commit()
		return redirect(request.args.get('next') or url_for('admin.index'))

	addteachform = AddTeachForm()
	if addteachform.validate_on_submit():
		ct = Teach(no=addteachform.tno.data,cname=addteachform.cname.data)
		db.session.add(ct)
		db.session.commit()
		return redirect(request.args.get('next') or url_for('admin.index'))
	"""
	while len(studentsform.users) > 0:
		studentsform.users.pop_entry()

	for student in students:
		studentform = UserForm()
		studentform.uid = student.id
		studentform.no = student.no
		studentform.username = student.name
		studentsform.users.append_entry(studentform)

	while len(teachersform.users) > 0:
		teachersform.users.pop_entry()

	for teacher in teachers:
		teacherform = UserForm()
		teacherform.uid = teacher.id
		teacherform.username = teacher.name
		teacherform.no = teacher.no
		teachersform.users.append_entry(teacherform)	
	"""

	ltc=[]
	for course in courses:
		tc={}
		tc['cname']=course.cname
		tc['chour'] = course.credithour
		tc['teachers'] = ''
		teas = Teach.query.filter_by(cname=course.cname).all()
		for tea in teas:
			u = User.query.filter_by(permission=1,no=tea.no).first()
			tc['teachers'] += u.name
		ltc.append(tc)


	if 'addstu' in request.form and request.method == 'POST':
		stu = User(no=request.form['sno'],name=request.form['sname'],permission=2)
		db.session.add(stu)
		db.session.commit()
		#return render_template('admin/admin.html',studentsform=studentsform,teachersform=teachersform)
		return redirect(request.args.get('next') or url_for('admin.index'))

	if 'addtea' in request.form and request.method == 'POST':
		tea = User(no=request.form['tno'],name=request.form['tname'],permission=1)
		db.session.add(tea)
		db.session.commit()
		return redirect(request.args.get('next') or url_for('admin.index'))

	if 'update' in request.form and request.method=='POST':
		u = User.query.filter_by(id=request.form['id']).first()
		if u is not None:
			u.no = request.form['no']
			u.name = request.form['name']
			db.session.add(u)
			db.session.commit()
			flash('have updated.')

	return render_template('admin/admin.html',students=students,
				teachers=teachers,ltc=ltc,
				addcourseform=addcourseform,
				addteachform=addteachform)

@admin.route('/deletes/<value>')
def deletes(value):
	u = User.query.filter_by(no=value,permission=2).first()
	db.session.delete(u)
	db.session.commit()
	flash("delete successfully.")
	return redirect(request.args.get('next') or url_for('admin.index'))

@admin.route("/deletet/<value>")
def deletet(value):
	u = User.query.filter_by(no=value,permission=1).first()
	db.session.delete(u)
	db.session.commit()
	flash("delete successfully.")
	return redirect(request.args.get('next') or url_for('admin.index'))


@admin.route('/resets/<value>')
def resets(value):
	u = User.query.filter_by(no=value,permission=2).first()
	db.session.password=None
	db.session.add(u)
	db.session.commit()
	flash("has reset.")
	return redirect(request.args.get('next') or url_for('admin.index'))

@admin.route("/resett/<value>")
def resett(value):
	u = User.query.filter_by(no=value,permission=1).first()
	u.password=None
	db.session.add(u)
	db.session.commit()
	flash("has reset.")
	return redirect(request.args.get('next') or url_for('admin.index'))