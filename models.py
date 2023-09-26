from app import db
from flask_login import UserMixin
    
### models from app.py below

class Roles(db.Model):
    role_id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(25), nullable=False)

class Majors(db.Model):
    major_id = db.Column(db.Integer, primary_key=True)
    major_name = db.Column(db.String(25), nullable=False)

class Degrees(db.Model):
    degree_id = db.Column(db.Integer, primary_key=True)
    degree_name = db.Column(db.String(25), nullable=False)

class Users(UserMixin, db.Model):
    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True)
    user_fname = db.Column(db.String(25), nullable=False)
    user_lname = db.Column(db.String(25), nullable=False)
    user_email = db.Column(db.String(25), unique=True, nullable=False)
    # password is unique can change later
    pwd = db.Column(db.String(300), nullable=False, unique=True)
    role = db.Column(db.Integer, db.ForeignKey("roles.role_id"), nullable=False)
    major = db.Column(db.Integer, db.ForeignKey("majors.major_id"), nullable=False)
    degree = db.Column(db.Integer, db.ForeignKey("degrees.degree_id"), nullable=False)
    gpa = db.Column(db.Numeric(3,2))
    hours = db.Column(db.Numeric(3,2))
    graduating_semester = db.Column(db.Integer)

    def __repr__(self):
        return '<User %r>' % self.user_email

class Courses(db.Model):
    course_id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String(25), nullable=False)

class Jobs(db.Model):
    job_id = db.Column(db.Integer, primary_key=True)
    job_name = db.Column(db.String(25), nullable=False)
    course_required = db.Column(db.Integer, db.ForeignKey("courses.course_id"))
    certification_required = db.Column(db.Boolean, nullable=False)
    status = db.Column(db.Boolean, nullable=False)

class Certifications(db.Model):
    cert_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))

class UserCourses(db.Model):
    uc_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    course_id = db.Column(db.Integer, db.ForeignKey("courses.course_id"))
    grade = db.Column(db.Numeric(5,2), nullable=False)

class Applications(db.Model):
    app_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    course_id = db.Column(db.Integer, db.ForeignKey("courses.course_id"))
    status = db.Column(db.Boolean, nullable=False)
    editable = db.Column(db.Boolean, nullable=False)
