from flask import Flask, render_template, redirect, url_for, flash, request
from flask_bootstrap import Bootstrap5
from GTAApplication import gta, db, login_manager  #, models, forms
from GTAApplication.forms import forms
from GTAApplication.models import models
from flask_login import login_required, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash


@login_manager.user_loader
def load_user(user_email):
    return models.Users.get(user_email)

@gta.route('/')
@login_required
def Home():
    return render_template("index.html")

@gta.route('/login')
def LoginPage():
    form = forms.LoginForm()
    return render_template("login.html", form=form)

@gta.route('/register')
def RegisterPage():
    result = db.session.execute(db.select(models.Roles.role_id, models.Roles.role_name).where(models.Roles.role_id > 1).where(models.Roles.role_id < 5)).all()
    roles = [("", "---")]
    [roles.append((r[0], r[1])) for r in result]
    #roles = [(r[0], r[1]) for r in result]
    result = db.session.execute(db.select(models.Majors.major_id, models.Majors.major_name)).all()
    majors = [("", "---")]
    [majors.append((r[0], r[1])) for r in result]
    #majors = [(r[0], r[1]) for r in result]
    result = db.session.execute(db.select(models.Degrees.degree_id, models.Degrees.degree_name)).all()
    degrees = [("", "---")]
    [degrees.append((r[0], r[1])) for r in result]
    #degrees = [(r[0], r[1]) for r in result]
    form = forms.RegisterForm()
    form.user_role.choices = roles
    form.user_major.choices = majors
    form.user_degree.choices = degrees
    return render_template("register.html", form=form)

@gta.route('/jobs')
@login_required
def JobsPage():
    return render_template('jobs.html')

@gta.route('/applications')
@login_required
def ApplicationsPage():
    return render_template('applications.html')

@gta.route('/admin')
@login_required
def AdminPage():
    return render_template('admin.html')

@gta.route('/account')
def AccountPage():
    return render_template('account.html')

@gta.route('/authlog', methods=['POST'])
def authlog():
    form = forms.LoginForm()
    if request.method == 'POST':
        u = models.Users.query.filter_by(user_email=request.form['user_email']).first()
        print(u.user_email, u.user_pass)
        print(request.form['user_pass'])
        if check_password_hash(u.user_pass, request.form['user_pass']):
            login_user(u)
        else:
            flash("Invalid Email or Password")

@gta.route('/authreg', methods=["POST", "GET"])
def authreg():
    print(request.form)
    form = forms.RegisterForm()

    result = db.session.execute(db.select(models.Roles.role_id, models.Roles.role_name).where(models.Roles.role_id > 1).where(models.Roles.role_id < 5)).all()
    roles = [("", "---")]
    [roles.append((r[0], r[1])) for r in result]
    #roles = [(r[0], r[1]) for r in result]
    result = db.session.execute(db.select(models.Majors.major_id, models.Majors.major_name)).all()
    majors = [("", "---")]
    [majors.append((r[0], r[1])) for r in result]
    #majors = [(r[0], r[1]) for r in result]
    result = db.session.execute(db.select(models.Degrees.degree_id, models.Degrees.degree_name)).all()
    degrees = [("", "---")]
    [degrees.append((r[0], r[1])) for r in result]
    #degrees = [(r[0], r[1]) for r in result]
    form = forms.RegisterForm()

    # Set choices (not user's selection, but all possible choices)
    form.user_role.choices = roles
    form.user_major.choices = majors
    form.user_degree.choices = degrees

    print(form.user_role.choices)
    print(form.user_major.choices)
    print(form.user_degree.choices)
    print(form.validate_on_submit())
    if form.validate_on_submit():
        existing_user = models.Users.query.filter_by(user_id=form.user_id.data).first()
        print(existing_user)
        if existing_user:
            flash('User ID already exists', 'error')
            return redirect(url_for('authreg'))
        nu = models.Users(
            user_id=form.user_id.data,
            user_fname=form.user_fname.data,
            user_lname=form.user_lname.data,
            user_email=form.user_email.data,
            role=form.user_role.data,
            major=form.user_major.data,
            degree=form.user_degree.data,
            user_pass=generate_password_hash(form.user_pass.data, method='sha256')
        )
        db.session.add(nu)
        try:
            db.session.commit()
            # Query the database for the user with the provided email or ID
            created_user = models.Users.query.filter_by(user_email=form.user_email.data).first()
            if created_user:
                print(f"User {created_user.user_id} created successfully")
                flash('Registration successful', 'success')
                return redirect(url_for('login')) # Replace 'login' with the actual login route endpoint
            else:
                print("User creation failed")
                flash('Registration failed due to database error', 'error')
        except Exception as e:
            db.session.rollback()
            flash('Registration failed due to database error', 'error')
    return render_template("login.html", form=form)

