from flask import Flask, render_template, redirect
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, EmailField, SelectField, DecimalField, SubmitField, PasswordField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.secret_key = 'dev'
bootstrap = Bootstrap5(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["FLASK_ENV"] = "development"
app.config["DEBUG"] = True
db = SQLAlchemy()
db.init_app(app)

class Roles(db.Model):
    __tablename__ = "Roles"
    role_id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(25), nullable=False)

class Majors(db.Model):
    major_id = db.Column(db.Integer, primary_key=True)
    major_name = db.Column(db.String(25), nullable=False)

class Degrees(db.Model):
    degree_id = db.Column(db.Integer, primary_key=True)
    degree_name = db.Column(db.String(25), nullable=False)

class Courses(db.Model):
    course_id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String(25), nullable=False)

class Jobs(db.Model):
    job_id = db.Column(db.Integer, primary_key=True)
    job_name = db.Column(db.String(25), nullable=False)
    course_required = db.Column(db.Integer, db.ForeignKey("Courses.course_id"))
    certification_required = db.Column(db.Boolean, nullable=False)
    status = db.Column(db.Boolean, nullable=False)

class Users(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    user_fname = db.Column(db.String(25), nullable=False)
    user_lname = db.Column(db.String(25), nullable=False)
    user_email = db.Column(db.String(25), nullable=False)
    role = db.Column(db.Integer, db.ForeignKey("Roles.role_id"), nullable=False)
    major = db.Column(db.Integer, db.ForeignKey("Majors.major_id"), nullable=False)
    degree = db.Column(db.Integer, db.ForeignKey("Degrees.degree_id"), nullable=False)
    gpa = db.Column(db.Numeric(3,2))
    hours = db.Column(db.Numeric(3,2))
    graduating_semester = db.Column(db.Integer)

class Certifications(db.Model):
    cert_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("Users.user_id"))

class UserCourses(db.Model):
    uc_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("Users.user_id"))
    course_id = db.Column(db.Integer, db.ForeignKey("Courses.course_id"))
    grade = db.Column(db.Numeric(5,2), nullable=False)

class Applications(db.Model):
    app_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("Users.user_id"))
    course_id = db.Column(db.Integer, db.ForeignKey("Courses.course_id"))
    status = db.Column(db.Boolean, nullable=False)
    editable = db.Column(db.Boolean, nullable=False)
    

class RegisterForm(FlaskForm):
    user_id = IntegerField("User ID", validators=[DataRequired()])
    user_fname = StringField("First Name", validators=[DataRequired()])
    user_lname = StringField("Last Name", validators=[DataRequired()])
    user_email = EmailField("Email", validators=[DataRequired()])
    user_role = SelectField("Role", coerce=str, validators=[DataRequired()])
    user_major = SelectField("Major", validators=[DataRequired()])
    user_degree = SelectField("Degree", validators=[DataRequired()])
    user_gpa = DecimalField("GPA", places=2)
    user_hours = DecimalField("Hours", places=2)
    user_pass = PasswordField()
    submit = SubmitField()

class LoginForm(FlaskForm):
    user_email = EmailField("Email", validators=[DataRequired()])
    user_pass = PasswordField()
    submit = SubmitField()


@app.route('/')
def Home():
    return render_template("index.html")

@app.route('/login')
def Login():
    form = LoginForm()
    return render_template("login.html", form=form)

@app.route('/register')
def Register():
    result = db.session.execute(db.select(Roles.role_id, Roles.role_name).where(Roles.role_id > 1).where(Roles.role_id < 5)).all()
    roles = [("", "---")]
    [roles.append((r[0], r[1])) for r in result]
    #roles = [(r[0], r[1]) for r in result]
    result = db.session.execute(db.select(Majors.major_id, Majors.major_name)).all()
    majors = [("", "---")]
    [majors.append((r[0], r[1])) for r in result]
    #majors = [(r[0], r[1]) for r in result]
    result = db.session.execute(db.select(Degrees.degree_id, Degrees.degree_name)).all()
    degrees = [("", "---")]
    [degrees.append((r[0], r[1])) for r in result]
    #degrees = [(r[0], r[1]) for r in result]
    form = RegisterForm()
    form.user_role.choices = roles
    form.user_major.choices = majors
    form.user_degree.choices = degrees
    return render_template("register.html", form=form)

@app.route('/auth', methods=["POST", "GET"])
def auth():
    print("Placeholder to test pages")
    form = RegisterForm()
    if form.validate_on_submit:
        print(form.data)
    return redirect("/")
    
if __name__ == '__main__':
    app.run()