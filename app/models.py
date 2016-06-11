from werkzeug.security import generate_password_hash, check_password_hash
from flask.ext.login import UserMixin,AnonymousUserMixin
from . import db, login_manager


class User(UserMixin,db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key=True)
    no = db.Column(db.String(10), unique=True,nullable=False)
    name= db.Column(db.String(10),nullable=False)
    password_hash = db.Column(db.String(128))
    permission = db.Column(db.Integer)
    grade = db.Column(db.Float)
    info = db.Column(db.String(64))

    #role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')
    
    @password.setter
    def password(self,password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id})

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True

    def can(self,permission):
        if self.permission<permission:
            return True
        else:
            return False


    def __repr__(self):
        return '<User %r>' % self.id

class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False


@login_manager.user_loader
def load_user(id):
    return User.query.get(id)

class Course(db.Model):
    __tablename__ = 'courses'
    id = db.Column(db.Integer,primary_key=True)
    cname = db.Column(db.String(10),nullable=False,unique=True)
    credithour = db.Column(db.Float)

class Learn(db.Model):
    __tablename__='learning'
    id = db.Column(db.Integer,primary_key=True)
    no = db.Column(db.String(10),db.ForeignKey('users.no')) #student number
    lesson = db.Column(db.Integer,db.ForeignKey('teaching.id'))
    grade = db.Column(db.Float)

class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer,primary_key=True)
    test = db.Column(db.Boolean)
    lesson = db.Column(db.Integer,db.ForeignKey('teaching.id'))


class  Teach(db.Model):
    __tablename__ = 'teaching'
    id = db.Column(db.Integer,primary_key=True)#lesson_id
    no = db.Column(db.String(10),db.ForeignKey('users.no'))#Teacher number
    cname = db.Column(db.String(10),db.ForeignKey('courses.cname'))
    weigh = db.Column(db.Integer)

class Grade(db.Model):
    __tablename__ = 'grades'
    id = db.Column(db.Integer,primary_key=True)
    no = db.Column(db.String(10),db.ForeignKey('users.no'))
    taskid = db.Column(db.Integer,db.ForeignKey('tasks.id'))
    grade = db.Column(db.Float)