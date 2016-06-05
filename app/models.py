from werkzeug.security import generate_password_hash, check_password_hash
from flask.ext.login import UserMixin
from . import db, login_manager

class Teacher(UserMixin, db.Model):
    __tablename__ = 'teachers'
    id = db.Column(db.Integer,primary_key=True)
    tno = db.Column(db.String(10), unique=True)
    name = db.Column(db.String(64))
    password_hash = db.Column(db.String(128))
    #users = db.relationship('User', backref='role', lazy='dynamic')

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')
    
    @password.setter
    def password(self,password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<Teacher %r>' % self.id


class Student(UserMixin,db.Model):
    __tablename__ = 'students'
    id = db.Column(db.Integer,primary_key=True)
    sno = db.Column(db.String(10), unique=True)
    name= db.Column(db.String(64))
    password_hash = db.Column(db.String(128))
    #role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')
    
    @password.setter
    def password(self,password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<Student %r>' % self.id

@login_manager.user_loader
def load_user(id):
    return Student.query.get(id)

class Course(db.Model):
    __tablename__='courses'
    id = db.Column(db.Integer,primary_key=True)
    sno = db.Column(db.String(10),db.ForeignKey('students.sno'))
    cname = db.Column(db.String)
    credithour = db.Column(db.Numeric(2,1))

class Task(db.Model):
    __tablename__ = 'task'
    id = db.Column(db.Integer,primary_key=True)
    sno = db.Column(db.String(10),db.ForeignKey('students.sno'))
    cname = db.Column(db.String,db.ForeignKey('courses.cname'))
    grade = db.Column(db.Numeric(3,2))

class Test(db.Model):
    __tablename__ = 'tests'
    id = db.Column(db.Integer,primary_key=True)
    sno = db.Column(db.String(10),db.ForeignKey('students.sno'))
    cname = db.Column(db.String,db.ForeignKey('courses.cname'))
    grade = db.Column(db.Numeric(3,2))

class  Teach(db.Model):
    __tablename__ = 'teach'
    id = db.Column(db.Integer,primary_key=True)
    tno = db.Column(db.String(10),db.ForeignKey('teachers.tno'))
    cname = db.Column(db.String,db.ForeignKey('courses.cname'))
