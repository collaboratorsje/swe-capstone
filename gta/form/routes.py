from flask import render_template, redirect, url_for, flash, request, session, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from flask_login import login_user, login_required, current_user
from flask_login.mixins import AnonymousUserMixin
from gta.extensions import db, DBUser, DBJob, CourseScore
from flask import current_app as app
from gta.form import bp as fbp
from gta.form.forms import LoginForm, RegisterForm, JobForm, ApplyForm, AddUserCourseForm, UpdateProfileForm
from gta.model.models import Users, Jobs, Majors, Degrees, Roles, Courses, Applications, UserCourses
import os

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
        if u and check_password_hash(u.user_pass, form.user_pass.data):
            login_user(u)
            return redirect(request.form['nextpage'])
        else:
            flash("Invalid Email or Password.", 'warning')
            return redirect(url_for('form.LoginPage'))
    return render_template("login.html", form=form, next=nextp)

@fbp.route('/register', methods=['POST', 'GET'])
def RegisterPage():
    form = RegisterForm()
    uform = AddUserCourseForm()
    if form.validate_on_submit and request.method == 'POST':
        print("In Validate", form.user_id.data)
        res = db.session.execute(db.select(Users.user_id).where(Users.user_id==int(form.user_id.data))).first()
        if res is None:
            courses = []
            nu = Users(
                # add more fields to go with the register form we will update
                user_id=form.user_id.data,
                user_fname=form.user_fname.data,
                user_lname=form.user_lname.data,
                user_email=form.user_email.data,
                role=2,
                major=form.user_major.data,
                degree=form.user_degree.data,
                gpa = form.user_gpa.data,
                hours = form.user_hours.data,
                user_pass=generate_password_hash(form.user_pass.data, method='scrypt')
            )
            print(nu)
            ucourses = uform.ucourses.data
            ucourses = uform.ucourses.data.split("|")
            for u in ucourses:
                if u == '':
                    ucourses.remove(u)
                else:
                    cs = u.split(",")
                    uc = UserCourses(
                        user_id = form.user_id.data,
                        course_id = cs[0],
                        grade = cs[1]
                    )
                    print(uc)
                    courses.append(uc)
            try:
                db.session.add(nu)
                [db.session.add(course) for course in courses]
                db.session.commit()
                print("Inserted")
            except Exception as e:
                print(e, "Error Writing to DB")
                db.session.rollback()
            finally:
                ucourses.clear()
        else:
            print("User Exists")
            return redirect(url_for("form.RegisterPage"))
        return redirect(url_for("form.LoginPage"))

    return render_template("register.html", form=form, courseform=uform, ucourses=None)

@fbp.route('/adducourse', methods=['POST', 'GET'])
def AddCourses():
    uform = AddUserCourseForm()
    courses = []
    if request.method == 'POST' and uform.validate_on_submit():
        print(uform.ucourses.data)
        ucourses = uform.ucourses.data.split("|")
        for u in ucourses:
            if u == '':
                ucourses.remove(u)
            else:
                cs = u.split(",")
                c = {
                    "course_id": int(cs[0]),
                    "course": uform.course_id.choices[int(cs[0])][1],
                    "grade": cs[1]
                }
                courses.append(c)
        jsonify(print(courses))
        return jsonify(courses.pop())

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
@fbp.route('/apply/<job_id>', methods=['POST', 'GET'])
def Apply(job_id):
    try:
        u = db.session.execute(db.Select(Users.user_id, Users.user_fname, Users.user_lname, Users.user_email, Users.major, Majors.major_name, Users.degree, Degrees.degree_name, Users.gpa, Users.hours).where(session['_user_id'] == Users.user_id).where(Users.major == Majors.major_id).where(Users.degree == Degrees.degree_id)).first()
    
        user = DBUser(u)
        j = db.session.execute(db.Select(Jobs.job_id, Roles.role_name, Jobs.course_required, Courses.course_name, Courses.course_level, Jobs.certification_required, Jobs.status).where(Jobs.job_id == job_id).where(Jobs.role_id == Roles.role_id).where(Jobs.course_required == Courses.course_id)).first()
        #print(j)
        job = DBJob(j)
        form = ApplyForm()
        form.user_id.default = user.user_id
        form.user_fname.default = user.user_fname
        form.user_lname.default = user.user_lname
        form.user_email.default = user.user_email
        form.user_major.default = user.major_id
        form.user_degree.default = user.degree_id
        form.user_gpa.default = user.user_gpa
        form.user_hours.default = user.user_hours 
        form.process()
        if form.validate_on_submit and request.method == 'POST':
            # Ensure the 'uploads' directory exists
            uploads_dir = os.path.join(app.root_path, 'uploads')
            print(f"Uploads directory path: {uploads_dir}")
            if not os.path.exists(uploads_dir):
                os.makedirs(uploads_dir)
            try:
                gfn = str(session['_user_id']) + "_gta_" + secure_filename(request.files['gta_cert'].filename)
                tfn = str(session['_user_id']) + "_transcript_" + secure_filename(request.files['transcript'].filename)

                gta_cert_path = os.path.join(uploads_dir, gfn)
                transcript_path = os.path.join(uploads_dir, tfn)

                request.files['gta_cert'].save(gta_cert_path)
                request.files['transcript'].save(transcript_path)

                apl = Applications(
                    user_id=user.user_id,
                    course_id=job.course_id,
                    status=job.status,
                    editable=False,
                    gta_cert=request.files['gta_cert'].read(),
                    transcript=request.files['transcript'].read(),
                    job_id=job.job_id
                )
                try:
                    db.session.add(apl)
                    db.session.commit()
                    print("Commited Application")
                except Exception as e:
                    print(f"Insert Error:\n{e}")    
            except Exception as e:
                print(f"Error: {e}")
                db.session.rollback()
                # Handle the error appropriately (e.g., display an error message to the user)

            return redirect(url_for('main.Home'))
    
        return render_template("apply.html", form=form, job=job)
    except:
        return redirect(url_for("form.LoginPage"))
@login_required 
@fbp.route('/profile', methods=['POST', 'GET'])
def ProfilePage():
    form = UpdateProfileForm()
    uform = AddUserCourseForm()
    print(current_user)
    if isinstance(current_user, AnonymousUserMixin):
        return redirect(url_for("form.LoginPage"))
    # Check for form submission and validation
    if form.validate_on_submit():
        # Update the current_user's attributes with the form data

        if form.user_email.data:
            user_with_email = Users.query.filter_by(user_email=form.user_email.data).first()
            if user_with_email and user_with_email.user_id != current_user.user_id:
                flash('Email is already in use by another account. Please choose a different email.', 'danger')
                return render_template('profile.html', form=form, courseform=uform)
            current_user.user_email = form.user_email.data

        if form.user_fname.data:
            current_user.user_fname = form.user_fname.data

        if form.user_lname.data:
            current_user.user_lname = form.user_lname.data

        if form.user_major.data and form.user_major.data != "":
            current_user.major = form.user_major.data

        if form.user_degree.data and form.user_degree.data != "":
            current_user.degree = form.user_degree.data

        if form.user_gpa.data is not None:  # Check for None because 0 is a valid value for GPA
            current_user.gpa = form.user_gpa.data

        if form.user_hours.data is not None:  # Same reason as above
            current_user.hours = form.user_hours.data

        # Password and email changing need addressed

        # Commit the changes to the database
        try:
            db.session.commit()
        except Exception as e:
            print(f"Failed to Access database: { e }")
            db.session.rollback()
        # Give feedback to the user
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('form.ProfilePage'))

    return render_template('profile.html', form=form, courseform=uform)


'''
@login_required
@fbp.route('/myaccount', methods=['POST', 'GET'])
def MyAccount():
    form = RegisterForm()
    u = db.session.execute(db.Select(Users.user_id, Users.user_fname, Users.user_lname, Users.user_email, Majors.major_name, Degrees.degree_name, Users.gpa, Users.hours).where(session['_user_id'] == Users.user_id).where(Users.major == Majors.major_id).where(Users.degree == Degrees.degree_id)).first()
'''
