from . import db

class Teacher(db.Model):
    __tablename__ = 'teachers'
    tno = db.Column(db.String(10), primary_key=True)
    tname = db.Column(db.String(64))
    #users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Teacher %r>' % self.tno


class Student(db.Model):
    __tablename__ = 'students'
    sno = db.Column(db.String(10), primary_key=True)
    sname= db.Column(db.String(64))
    #role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<Student %r>' % self.sno


