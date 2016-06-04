from flask import render_template
from . import main

@main.route('/')
def index():
    '''
    form = NameForm()
    if form.validate_on_submit():
        stu = Student.query.filter_by(sno=form.name.data).first()
        if  stu is None:
            stu = Student(sno=form.name.data)
            db.session.add(stu)
            session['known'] = False
        else:
            session['known'] = True
        session['name'] = form.name.data
        return redirect(url_for('.index'))
    return render_template('index.html', form=form, name=session.get('name'),
                           known=session.get('known', False))
    '''
    return render_template('index.html')
