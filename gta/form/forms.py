from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, EmailField, SelectField, DecimalField, SubmitField, PasswordField, HiddenField, BooleanField
from wtforms.validators import DataRequired
from gta.extensions import db
from gta.model.models import Roles, Majors, Degrees, Courses
from flask import current_app as app

class RegisterForm(FlaskForm):
    #with app.app_context():
    with app.app_context():
        resr = db.session.execute(db.select(Roles.role_id, Roles.role_name).where(Roles.role_id > 1).where(Roles.role_id < 5)).all()
        resm = db.session.execute(db.select(Majors.major_id, Majors.major_name)).all()
        resd = db.session.execute(db.select(Degrees.degree_id, Degrees.degree_name)).all()
    roles = [(r[0], r[1]) for r in resr]
    roles.insert(0, ("", "---"))
    majors = [(r[0], r[1]) for r in resm]
    majors.insert(0, ("", "---"))
    degrees = [(r[0], r[1]) for r in resd]
    degrees.insert(0, ("", "---"))
    user_id = IntegerField("User ID", validators=[DataRequired()])
    user_fname = StringField("First Name", validators=[DataRequired()])
    user_lname = StringField("Last Name", validators=[DataRequired()])
    user_email = EmailField("Email", validators=[DataRequired()])
    user_role = SelectField("Role", coerce=str, choices=roles,validators=[DataRequired()])
    user_major = SelectField("Major", coerce=str, choices=majors, validators=[DataRequired()])
    user_degree = SelectField("Degree", coerce=str, choices=degrees, validators=[DataRequired()])
    user_gpa = DecimalField("GPA", places=2)
    user_hours = DecimalField("Hours", places=2)
    user_pass = PasswordField()
    user_confirm_pass = PasswordField()
    submit = SubmitField()

class LoginForm(FlaskForm):
    user_email = EmailField("Email", validators=[DataRequired()])
    user_pass = PasswordField()
    next = HiddenField()
    submit = SubmitField()

class JobForm(FlaskForm):
    with app.app_context():
        resc = db.session.execute(db.select(Courses.course_id, Courses.course_name)).all()
    courses = [(r[0], r[1]) for r in resc]
    courses.insert(0, ("", "---"))
    job_id = IntegerField("Job ID", validators=[DataRequired()])
    job_name = StringField("Job Name", validators=[DataRequired()])
    course_required = SelectField("Course Required", coerce=str, choices=courses, validators=[DataRequired()])
    certification_required = BooleanField("Certification Y/N")
    # populate courses from db for course required field
    submit = SubmitField()

