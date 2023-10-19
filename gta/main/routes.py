from flask import render_template, redirect, url_for, session
from flask_login import login_required, logout_user
from gta.main import bp as mbp
from gta.model.models import Users, Jobs, Roles, Courses
from gta.extensions import login_manager
from flask_bootstrap import Bootstrap5
from flask import current_app as app
from gta.extensions import db

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

@mbp.route('/logout')
def Logout():
    logout_user()
    return redirect(url_for("main.Home"))

@mbp.route('/')
def Home():
    with app.app_context():
        resj = db.session.execute(db.select(Courses.course_name, Jobs.certification_required, Roles.role_name, Courses.course_level).where(Jobs.role_id == Roles.role_id).where(Jobs.course_required == Courses.course_id)).all()
    jobs = [r for r in resj]    
    return render_template("index.html", jobs=jobs)

@mbp.route('/jobs', methods=['GET'])
@login_required
def JobsPage():
    with app.app_context():
        resj = db.session.execute(db.select(Courses.course_name, Jobs.certification_required, Roles.role_name).where(Jobs.user_id == session["_user_id"]).where(Jobs.role_id == Roles.role_id).where(Jobs.course_required == Courses.course_id)).all()
    for r in resj:
        print(r)
    jobs = [r for r in resj]
    
    return render_template('jobs.html', jobs = resj)

@mbp.route('/applications', methods=['GET'])
@login_required
def ApplicationsPage():
    return render_template('applications.html')

@mbp.route('/admin')
@login_required
def AdminPage():
    return render_template('admin.html')

@mbp.route('/account')
def AccountPage():
    return render_template('account.html')