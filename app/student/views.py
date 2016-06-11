from flask import render_template, redirect, request, url_for, flash
from . import student
from .. import db
from ..models import User,Course,Teach,Learn,Grade

@student.route('/student/<userno>',methods=['GET','POST'])
@login_required
@student_required
def user(userno):
	user = User.query.filter_by(no=userno,permission=2).first()
	if user is None:
		abort(404)
	learns= Learn.query.filter_by(no=user.no).all()

	total_credit = 0
	stuview=[]
	for learn in learns:
		stuviewline={}
		stuviewline['grade']=learn.grade
		teachlearn = Teach.query.filter_by(id=learn.lesson).first()
		stuviewline['cname'] = teachlearn.cname
		course = Course.query.filter_by(cname=teachlearn.cname).first()
		stuviewline['chour'] = course.credithour
		total_credit += course.credithour
		stuview.append(stuviewline)

	if 'submit' in request.form and request.method=='POST':
		 return redirect(request.args.get('next') or url_for('student.lesson',user=userno))

	return  render_template('student/student.html',stuview=stuview,student=user,tc=total_credit) 

@student.route('/lesson/<user>',methods=['GET','POST'])
@login_required
@student_required
def lesson(user):
	student=User.query.filter_by(no=user,permission=2).first()
	teachs = Teach.query.all()
	learned = Learn.query.filter_by(no=student.no).all()
	choices=[]
	for teach in teachs:
		choice={}
		choice['id']=teach.id	#teach id
		choice['cname']=teach.cname	#course name
		teacher = User.query.filter_by(no=teach.no,permission=1).first()
		choice['tname']=teacher.name	#teacher.name
		course = Course.query.filter_by(cname=teach.cname).first()
		choice['chour']=course.credithour #credit hour
		choice['choosed']=False		#whether has choosed
		for learns in learned:
			if learns.lesson == teach.id:
				choice['choosed']=True	
				break
		choices.append(choice)
	
	if 'lesson' in request.form and request.method=='POST':
		if request.form['lesson'] == 'choose':
			newlearn = Learn(no=student.no,lesson=request.form['id'],grade=0)
			db.session.add(newlearn)
			db.session.commit()
		if request.form['lesson'] == 'delete':
			db.session.execute("PRAGMA foreign_keys=ON")
			oldlearn = Learn.query.filter_by(no=student.no,lesson=request.form['id']).first()
			db.session.delete(oldlearn)
			db.session.commit()
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
		return redirect(request.args.get('next') or url_for('student.lesson',user=user))


	return  render_template('student/lesson.html',choices=choices) 