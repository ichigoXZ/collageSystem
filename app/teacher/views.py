from flask import render_template, redirect, request, url_for, flash
from flask.ext.login import login_user, logout_user, login_required, \
    current_user
from . import teacher
from .. import db
from ..models import User,Course,Teach,Learn,Task,Grade
from .forms import taskForm
from ..decorators import teacher_required

@teacher.route('/teacher/<userno>',methods=['GET','POST'])
@login_required
@teacher_required
def user(userno):
    user = User.query.filter_by(no=userno).first()
    if user is None:
    	abort(404)
    teach = Teach.query.filter_by(no=userno).all()

    return render_template('teacher/teacher.html', user=user,teach=teach) 

@teacher.route('/task/<user>/<lessonid>',methods=['GET','POST'])
@login_required
@teacher_required
def task(lessonid,user):
	tasks = Task.query.filter_by(lesson=lessonid).all()
	learns = Learn.query.filter_by(lesson=lessonid).all()
	test = Task.query.filter_by(lesson=lessonid,test=True).all()

	ll = Task.query.filter_by(lesson=lessonid,test=True).count()
	tl = Task.query.filter_by(lesson=lessonid,test=False).count()

	teach = Teach.query.filter_by(no=user,id=lessonid).first()

	if 'add test'  in request.form   and request.method=='POST':
		db.session.execute("PRAGMA foreign_keys=ON")
		test = Task(lesson=lessonid,test=True)
		db.session.add(test)
		db.session.commit()
		return redirect(request.args.get('next') or url_for('teacher.task',user=user,lessonid=lessonid))

	if 'add task'  in request.form   and request.method=='POST':
		db.session.execute("PRAGMA foreign_keys=ON")
		test = Task(lesson=lessonid,test=False)
		db.session.add(test)
		db.session.commit()
		return redirect(request.args.get('next') or url_for('teacher.task',user=user,lessonid=lessonid))

	if 'set' in request.form and request.method=='POST':
		db.session.execute("PRAGMA foreign_keys=ON")
		teach.weigh = request.form['percent']
		db.session.add(teach)
		db.session.commit()
		return  redirect(request.args.get('next') or url_for('teacher.grade',user=user,lessonid=lessonid))

	if 'submit' in request.form and request.method == 'POST':	
		if request.form['submit'] == 'set':	
			for learn in learns:
				score = Grade.query.filter_by(no=learn.no,taskid=request.form['task']).first()
				if score is not None:
					db.session.execute("PRAGMA foreign_keys=ON")
					score.grade = request.form[learn.no]
					db.session.add(score)
					db.session.commit()
				else:
					db.session.execute("PRAGMA foreign_keys=ON")
					new = Grade(no=learn.no,taskid=request.form['task'],grade=request.form[learn.no])
					db.session.add(new)
					db.session.commit()
			return  redirect(request.args.get('next') or url_for('teacher.grade',user=user,lessonid=lessonid))
		if request.form['submit'] == 'view':
			grades = Grade.query.filter_by(taskid=request.form['task']).all()
			count = Grade.query.filter_by(taskid=request.form['task']).count()
			if count==0:
				flash("Have not scored yet!")
			else:
				return  render_template('teacher/task.html', tasks=tasks,learns=learns,grades=grades,tl=tl,
							ll=ll,teach=teach,view=True) 
		return redirect(request.args.get('next') or url_for('teacher.task',user=user,lessonid=lessonid))

	return  render_template('teacher/task.html', tasks=tasks,grades=learns,view=False,learns=learns,tl=tl,
							ll=ll,teach=teach) 

@teacher.route('/grade/<user>/<lessonid>')
@login_required
@teacher_required
def grade(user,lessonid):
	learns = Learn.query.filter_by(lesson=lessonid).all()
	teach = Teach.query.filter_by(id=lessonid).first()
	for learn in learns:
		test_score = 0
		task_score = 0
		test_num = 0
		task_num = 0
		for g,t in db.session.query(Grade,Task).filter(Grade.taskid==Task.id,Grade.no==learn.no,Task.lesson==lessonid).all():
			if t.test == True:
				test_score += g.grade
				test_num += 1
			else:
				task_score += g.grade
				task_num += 1
		learn.grade =  round((test_score*teach.weigh/test_num + task_score*(100-teach.weigh)/task_num)/100,3)
		db.session.add(learn)
		db.session.commit()
		student = User.query.filter_by(no=learn.no).first()
		total_score = 0
		chour = 0
		for l,t,c in db.session.query(Learn,Teach,Course).filter(Learn.no == student.no,
							Learn.lesson==Teach.id,
							Teach.cname==Course.cname):
			total_score += l.grade*c.credithour
			chour += c.credithour
		student.grade = total_score/chour
		db.session.add(student)
		db.session.commit()
	return  redirect(request.args.get('next') or url_for('teacher.task',user=teach.no,lessonid=teach.id))

