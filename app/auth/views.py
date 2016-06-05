from flask import render_template, redirect, request, url_for, flash
from flask.ext.login import login_user, logout_user, login_required, \
    current_user
from . import auth
from .. import db
from ..models import Student
from .forms import LoginForm, RegistrationForm



@auth.route('/login',methods=['GET','POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		stu = Student.query.filter_by(sno=form.sno.data).first()
		if stu is not None and stu.verify_password(form.password.data):
			login_user(stu, form.remember_me.data)
			return redirect(request.args.get('next') or url_for('main.index'))
		flash('Invalid sno or password.')
	return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
	logout_user()
	flash("You have been logged out.")
	return redirect(url_for('main.index'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        stu = Student.query.filter_by(sno=form.sno.data).first()
        if stu is not None:
        	stu.password=form.password.data
        	flash('You can now login.')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)
