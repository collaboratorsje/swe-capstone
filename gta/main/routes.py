from flask import render_template, redirect, url_for, session
from flask_login import login_required, logout_user
from gta.main import bp as mbp
from gta.model.models import Users, Jobs, Roles, Courses, Applications
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
    with app.app_context():
        resj = db.session.execute(db.select(Courses.course_name, Courses.course_level, Jobs.certification_required, Roles.role_name).where(Jobs.role_id == Roles.role_id).where(Jobs.course_required == Courses.course_id)).all()
        resa = db.session.execute(db.select(Users.user_id, Courses.course_name, Courses.course_level, Applications.status, Applications.status, Applications.gta_cert, Applications.transcript, Roles.role_name, Jobs.job_id).where(Applications.user_id == Users.user_id).where(Applications.course_id == Courses.course_id).where(Applications.job_id == Jobs.job_id).where(Jobs.role_id == Roles.role_id)).all()
    jobs = [{"course": r[0]+" - "+r[1], "cert_required": r[2], "role_name": r[3]} for r in resj]
    apps = [{"user_id": a[0], "course": a[1]+" - "+a[2], "status": a[3], "gta_cert": a[4], "transcript": a[5], "role": a[7], "job_id": a[8]} for a in resa]
    return render_template('admin.html',jobs=jobs, apps=apps)

@mbp.route('/account')
def AccountPage():
    return render_template('account.html')

@mbp.route('/profile')
@login_required
def ProfilePage():
    return render_template('profile.html')