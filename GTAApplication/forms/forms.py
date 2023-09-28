from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, EmailField, SelectField, DecimalField, SubmitField, PasswordField
from wtforms.validators import DataRequired

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
    user_confirm_pass = PasswordField()
    submit = SubmitField()

class LoginForm(FlaskForm):
    user_email = EmailField("Email", validators=[DataRequired()])
    user_pass = PasswordField()
    submit = SubmitField()