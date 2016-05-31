import os
import pymysql
from flask import Flask, render_template, session, redirect, url_for,flash
from flask.ext.script import Manager, Shell
from flask.ext.bootstrap import Bootstrap
from flask.ext.moment import Moment
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'

manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)
db = pymysql.connect(host="localhost",user="root",passwd="ting",db="CollageSystem",port=3306,charset="utf8")
curs = db.cursor()

class NameForm(Form):
    name = StringField('What is your name?', validators=[Required()])
    submit = SubmitField('Submit')


def make_shell_context():
    return dict(app=app, db=db)
manager.add_command("shell", Shell(make_context=make_shell_context))


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        name = form.name.data
        lines=None
        try:
            lines = curs.execute("select * from student where sno='%s'"%name)
        except:
            flash( "cannot select table")
        if lines == 0:
            session['known'] = False
        else:
            session['known'] = True
        session['name'] = form.name.data
        return redirect(url_for('index'))
    return render_template('index.html', form=form, name=session.get('name'),
                            known=session.get('known',False)) 
   # curs = db.cursor()
    """
    form = NameForm()
    if form.validate_on_submit():
        curs.execute("select * from student where sno='%s'"% form.name.data)
        lines = cur.fetchall()
        if lines is None:
            session['known'] = False
        else:
            session['known'] = True
        session['name'] = form.name.data
        return redirect(url_for('index'))
     """
   # return render_template('index.html', form=form, name=session.get('name'),
              #             known=session.get('known', False))


if __name__ == '__main__':
    manager.run()
