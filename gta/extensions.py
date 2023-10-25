from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
db = SQLAlchemy()
login_manager = LoginManager()

class DBUser:
    def __init__(self, u: tuple):
        self.user_id = u[0]
        self.user_fname = u[1]
        self.user_lname = u[2]
        self.user_email = u[3]
        self.major_id = u[4]
        self.major = u[5]
        self.degree_id = u[6]
        self.degree = u[7]
        self.user_gpa = u[8]
        self.user_hours = u[9]
    
    def __repr__(self):
        return f"<{self.user_id} {self.user_fname} {self.user_lname} {self.user_email}>"

class DBJob:
    def __init__(self, j: tuple):
        self.job_id = j[0]
        self.role = j[1]
        self.course_id = j[2]
        self.course_name = j[3]
        self.course_level = j[4]
        self.cert = j[5]
        self.status = j[6]

class CourseScore:
    def __init__(self, c: tuple):
        self.course_id = c[0]
        self.grade = c[1]
    
    def __repr__(self):
        return f"<{self.course_id}, {self.grade}>"