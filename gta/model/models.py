from flask_login import UserMixin
from gta.extensions import db

class Users(UserMixin, db.Model):
    __tablename__ = "Users"
    
    user_id = db.Column(db.Integer, primary_key=True)
    user_fname = db.Column(db.String(25), nullable=False)
    user_lname = db.Column(db.String(25), nullable=False)
    user_email = db.Column(db.String(25), nullable=False)
    role = db.Column(db.Integer, db.ForeignKey("Roles.role_id"), nullable=False)
    major = db.Column(db.Integer, db.ForeignKey("Majors.major_id"), nullable=False)
    degree = db.Column(db.Integer, db.ForeignKey("Degrees.degree_id"), nullable=False)
    gpa = db.Column(db.Numeric(3,2))
    hours = db.Column(db.Numeric(3,2))
    #graduating_semester = db.Column(db.Integer)
    user_pass = db.Column(db.String)

    def get_id(self):
        return self.user_id
    
    def __repr__(self):
        return f"<User {self.user_id}: {self.user_fname} {self.user_lname}, Email: {self.user_email}, Role: {self.role}>"

class Roles(db.Model):
    __tablename__ = "Roles"
    role_id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(25), nullable=False)

class Majors(db.Model):
    __tablename__ = "Majors"
    major_id = db.Column(db.Integer, primary_key=True)
    major_name = db.Column(db.String(25), nullable=False)

class Degrees(db.Model):
    __tablename__ = "Degrees"
    degree_id = db.Column(db.Integer, primary_key=True)
    degree_name = db.Column(db.String(25), nullable=False)

class Courses(db.Model):
    __tablename__ = "Courses"
    course_id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String(25), nullable=False)
    course_level = db.Column(db.String(50), nullable=False)
    major_id = db.Column(db.Integer, db.ForeignKey("Majors.major_id"))

class Jobs(db.Model):
    __tablename__ = "Jobs"
    job_id = db.Column(db.Integer,autoincrement=True, primary_key=True )
    role_id = db.Column(db.Integer, db.ForeignKey("Roles.role_id"))
    course_required = db.Column(db.Integer, db.ForeignKey("Courses.course_id"))
    certification_required = db.Column(db.Boolean, nullable=False)
    status = db.Column(db.Boolean, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("Users.user_id"))

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
    gta_cert = db.Column(db.BLOB)
    transcript = db.Column(db.BLOB, nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey("Jobs.job_id"))