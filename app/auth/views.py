from flask import render_template
from . import auth


@auth.route('/login',methods=['GETS','POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		stu = Student.query.filter_by(sno=form.sno.data).first()
		if stu is not None and stu.verify_password(form.password.data):
			login_student(stu,form.remember_me.data)
			return redirect(request.args.get('next') or url_for('main.index'))
		flash('Invalid sno or password')
	return render_template('auth/login.html',form=form)


@auth.route('/logout')
@login_required
def logout():
	logout_student()
	flash("You have been logged out.")
	return redirect(url_for('main.index'))