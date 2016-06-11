from flask import render_template, redirect, request, url_for, flash
from flask.ext.login import login_user, logout_user, login_required, \
    current_user
from . import admin
from .. import db
from ..models import User,Course,Teach
from .forms import AdminForm,AddUserForm,UserForm,AddCourseForm,AddTeachForm
from ..decorators import admin_required, permission_required

@admin.route('/',methods=['GET','POST'])
@login_required
@admin_required
def index():
	students = User.query.filter_by(permission=2).all()
	teachers = User.query.filter_by(permission=1).all()
	courses = Course.query.all()
	teaching = Teach.query.all()

	ltc=[]
	for course in courses:
		tc={}
		tc['cname']=course.cname
		tc['chour'] = course.credithour
		tc['teachers'] = ''
		teas = Teach.query.filter_by(cname=course.cname).all()
		for tea in teas:
			u = User.query.filter_by(permission=1,no=tea.no).first()
			if u is not None:
				tc['teachers'] += u.name 
				tc['teachers'] += ','
		ltc.append(tc)

	if 'delete' in request.form and request.method=='POST':
		db.session.execute("PRAGMA foreign_keys=ON")
		course = Course.query.filter_by(cname=request.form['id']).first()
		db.session.delete(course)
		db.session.commit()
		return redirect(request.args.get('next') or url_for('admin.index'))

	if 'addstu' in request.form and request.method == 'POST':
		db.session.execute("PRAGMA foreign_keys=ON")
		stu = User(no=request.form['sno'],name=request.form['sname'],permission=2)
		db.session.add(stu)
		db.session.commit()
		#return render_template('admin/admin.html',studentsform=studentsform,teachersform=teachersform)
		return redirect(request.args.get('next') or url_for('admin.index'))

	if 'addtea' in request.form and request.method == 'POST':
		db.session.execute("PRAGMA foreign_keys=ON")
		tea = User(no=request.form['tno'],name=request.form['tname'],permission=1)
		db.session.add(tea)
		db.session.commit()
		return redirect(request.args.get('next') or url_for('admin.index'))

	if 'update' in request.form and request.method=='POST':
		db.session.execute("PRAGMA foreign_keys=ON")
		u = User.query.filter_by(id=request.form['id']).first()
		if u is not None:
			u.no = request.form['no']
			u.name = request.form['name']
			db.session.add(u)
			db.session.commit()
			flash('have updated.')
		return redirect(request.args.get('next') or url_for('admin.index'))

	if 'course' in request.form and request.method == 'POST':
		flash('have updated.')
		db.session.execute("PRAGMA foreign_keys=ON")
		co = Course.query.filter_by(id = request.form['id']).first()
		co.cname = request.form['cname']
		co.credithour = request.form['credithour']
		db.session.add(co)
		db.session.commit()		
		return redirect(request.args.get('next') or url_for('admin.index'))

	if 'teach' in request.form and request.method == 'POST':
		db.session.execute("PRAGMA foreign_keys=ON")
		t = Teach.query.filter_by(id = request.form['id']).first()
		db.session.delete(t)
		db.session.commit()
		return redirect(request.args.get('next') or url_for('admin.index'))


	addcourseform = AddCourseForm()	
	if addcourseform.validate_on_submit():
		c = Course(cname=addcourseform.cname.data,credithour=addcourseform.credithour.data)
		db.session.add(c)
		db.session.commit()
		return redirect(request.args.get('next') or url_for('admin.index'))

	addteachform = AddTeachForm()
	if addteachform.validate_on_submit():
		db.session.execute("PRAGMA foreign_keys=ON")
		ct = Teach(no=addteachform.tno.data,cname=addteachform.cname.data)
		db.session.add(ct)
		db.session.commit()
		return redirect(request.args.get('next') or url_for('admin.index'))
	
	return render_template('admin/admin.html',students=students,
				teachers=teachers,ltc=ltc,
				addcourseform=addcourseform,
				addteachform=addteachform,
				courses=courses,
				teachs=teaching)

@admin.route('/deletes/<value>')
@login_required
@admin_required
def deletes(value):
	db.session.execute("PRAGMA foreign_keys=ON")
	u = User.query.filter_by(no=value,permission=2).first()
	db.session.delete(u)
	db.session.commit()
	flash("delete successfully.")
	return redirect(request.args.get('next') or url_for('admin.index'))

@admin.route("/deletet/<value>")
@login_required
@admin_required
def deletet(value):
	db.session.execute("PRAGMA foreign_keys=ON")
	u = User.query.filter_by(no=value,permission=1).first()
	db.session.delete(u)
	db.session.commit()
	flash("delete successfully.")
	return redirect(request.args.get('next') or url_for('admin.index'))


@admin.route('/resets/<value>')
@login_required
@admin_required
def resets(value):
	u = User.query.filter_by(no=value,permission=2).first()
	u.password = '111'
	db.session.add(u)
	db.session.commit()
	flash("has reset.")
	return redirect(request.args.get('next') or url_for('admin.index'))

@admin.route("/resett/<value>")
@login_required
@admin_required
def resett(value):
	u = User.query.filter_by(no=value,permission=1).first()
	u.password='111'
	db.session.add(u)
	db.session.commit()
	flash("has reset.")
	return redirect(request.args.get('next') or url_for('admin.index'))