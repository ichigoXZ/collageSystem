from flask import render_template, redirect, request, url_for, flash
from flask.ext.login import login_user, logout_user, login_required, \
    current_user
from . import auth
from .. import db
from ..models import User
from .forms import LoginForm, RegistrationForm,ChangePasswordForm

@auth.route('/login',methods=['GET','POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		if form.select.data=='Teacher':
			user = User.query.filter_by(no=form.no.data,permission=1).first()
			if user is not None and user.verify_password(form.password.data):
				login_user(user,form.remember_me.data)
				return redirect(request.args.get('next') or url_for('teacher.user',userno=current_user.no))
			flash('Invalid tno or password')
			flash("Register if you are first here.")			
		if form.select.data=='Student':
			user = User.query.filter_by(no=form.no.data,permission=2).first()
			if user is not None and user.verify_password(form.password.data):
				login_user(user, form.remember_me.data)
				return redirect(request.args.get('next') or url_for('student.user',userno=current_user.no))
			flash('Invalid sno or password.')
			flash("Register if you are first here.")
		if form.select.data == 'Administrator':
			user = User.query.filter_by(no=form.no.data,permission=0).first()
			if user is not None and user.verify_password(form.password.data):
				login_user(user, form.remember_me.data)
				return redirect(request.args.get('next') or url_for('admin.index'))
			flash('Invalid adminno or password.')
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
		if form.tstype.data:
			user = User.query.filter_by(no=form.no.data,permission=1).first()
			if user is not None:
				if user.password_hash:
					flash('This teacher has already registered.')
				else:
					user.password=form.password.data
					flash('You can now login.')
					return redirect(url_for('auth.login'))
			else:
				flash('No such teacher in collage.')
		else:
			user = User.query.filter_by(no=form.no.data).first()
			if user is not None:
				if user.password_hash:
					flash('This student has already registered.')
				else:
					user.password=form.password.data
					flash('You can now login.')
					return redirect(url_for('auth.login'))
			else:
				flash('No such student in collage.')
	return render_template('auth/register.html', form=form)

@auth.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            current_user.password = form.password.data
            db.session.add(current_user)
            flash('Your password has been updated.')
            return redirect(url_for('main.index'))
        else:
            flash('Invalid password.')
    return render_template("auth/change_password.html", form=form)