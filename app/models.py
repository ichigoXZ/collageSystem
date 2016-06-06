from werkzeug.security import generate_password_hash, check_password_hash
from flask.ext.login import UserMixin
from . import db, login_manager


class User(UserMixin,db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key=True)
    no = db.Column(db.String(10), unique=True)
    name= db.Column(db.String(10))
    password_hash = db.Column(db.String(128))
    permission = db.Column(db.Integer)
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
    return User.query.get(id)

class Course(db.Model):
    __tablename__ = 'courses'
    id = db.Column(db.Integer,primary_key=True)
    cname = db.Column(db.String)
    credithour = db.Column(db.Numeric(2,1))

class Learn(db.Model):
    __tablename__='learning'
    id = db.Column(db.Integer,primary_key=True)
    no = db.Column(db.String(10),db.ForeignKey('users.no'))
    cname = db.Column(db.String,db.ForeignKey('courses.cname'))


class Task(db.Model):
    __tablename__ = 'task'
    id = db.Column(db.Integer,primary_key=True)
    no = db.Column(db.String(10),db.ForeignKey('users.no'))
    cname = db.Column(db.String,db.ForeignKey('courses.cname'))
    grade = db.Column(db.Numeric(3,2))

class Test(db.Model):
    __tablename__ = 'tests'
    id = db.Column(db.Integer,primary_key=True)
    no = db.Column(db.String(10),db.ForeignKey('users.no'))
    cname = db.Column(db.String,db.ForeignKey('courses.cname'))
    grade = db.Column(db.Numeric(3,2))

class  Teach(db.Model):
    __tablename__ = 'teaching'
    id = db.Column(db.Integer,primary_key=True)
    no = db.Column(db.String(10),db.ForeignKey('users.no'))
    cname = db.Column(db.String,db.ForeignKey('courses.cname'))
