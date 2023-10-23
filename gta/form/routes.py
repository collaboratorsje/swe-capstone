from flask import render_template, redirect, url_for, flash, request, session
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user, login_required
from gta.extensions import db
from gta.form import bp as fbp
from gta.form.forms import LoginForm, RegisterForm, JobForm
from gta.model.models import Users, Jobs

@fbp.route('/login', methods=['POST', 'GET'])
def LoginPage():
    form = LoginForm()
    nextp = None
    if request.method == 'GET':
        try:
            nextp = request.args['next']
        except:
            nextp = '/'
    if form.validate_on_submit and request.method == 'POST':
        u = Users.query.filter_by(user_email=form.user_email.data).first()
        print(u)
        if check_password_hash(u.user_pass, form.user_pass.data):
            login_user(u)
            return redirect(request.form['nextpage'])
        else:
            flash("Incorrect User or Password")
            return redirect(url_for('LoginPage'))
    return render_template("login.html", form=form, next=nextp)

@fbp.route('/register', methods=['POST', 'GET'])
def RegisterPage():
    form = RegisterForm()
    if form.validate_on_submit and request.method == 'POST':
        print("In Validate", form.user_id.data)
        res = db.session.execute(db.select(Users.user_id).where(Users.user_id==int(form.user_id.data))).first()
        print(res)
        if res is None:
            nu = Users(
                # add more fields to go with the register form we will update
                user_id=form.user_id.data,
                user_fname=form.user_fname.data,
                user_lname=form.user_lname.data,
                user_email=form.user_email.data,
                role=form.user_role.data,
                major=form.user_major.data,
                degree=form.user_degree.data,
                user_pass=generate_password_hash(form.user_pass.data, method='sha256')
            )
            print(nu)
            db.session.add(nu)
            try:
                db.session.commit()
                print("Inserted")
            except:
                print("Error Writing to DB")
                db.session.rollback()
        else:
            print("User Exists")
            return redirect(url_for("form.RegisterPage"))
        return redirect(url_for("form.LoginPage"))
    return render_template("register.html", form=form)

@login_required
@fbp.route('/createjob', methods=['POST', 'GET'])
def CreateJobPage():
    form = JobForm()
    if form.validate_on_submit and request.method == 'POST':
        #jobObj = db.session.execute(db.select(Jobs.job_id).where(Jobs.job_id==int(form.job_id.data))).first()
        #print(jobObj)
        jobObj = None
        if jobObj is None:
            tempJob = Jobs(
                role_id = form.role.data,
                course_required=form.course_required.data,
                certification_required=form.certification_required.data,
                status=False,
                user_id = session['_user_id']
            )
            print(tempJob, tempJob.user_id)
            try:
                db.session.add(tempJob)
                db.session.commit()
                print("Created job successfully")
            except Exception as e:
                print(e, "Error Writing to DB")
                db.session.rollback()
        else:
            print("Job Exists")
            return redirect(url_for("form.CreateJobPage"))
        return redirect(url_for("main.JobsPage"))
    return render_template("createjob.html", form=form)

@login_required
@fbp.route('/apply')
def Apply():
    #form = ApplyForm()
    print("in Apply")
@login_required
@fbp.route('/myaccount', methods=['POST', 'GET'])
def MyAccount():
    form = RegisterForm()
    user = db.session.execute(db.Select(Users.user_id).where(session['_current_user'] == Users)).all()