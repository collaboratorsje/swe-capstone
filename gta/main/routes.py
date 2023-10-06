from flask import render_template, redirect, url_for
from flask_login import login_required, logout_user
from gta.main import bp as mbp
from gta.model.models import Users
from gta.extensions import login_manager
from flask_bootstrap import Bootstrap5

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

@mbp.route('/logout')
def Logout():
    logout_user()
    return redirect(url_for("main.Home"))

@mbp.route('/')
def Home():
    return render_template("index.html")

@mbp.route('/jobs', methods=['GET'])
@login_required
def JobsPage():
    return render_template('jobs.html')

@mbp.route('/applications', methods=['GET'])
@login_required
def ApplicationsPage():
    return render_template('applications.html')

@mbp.route('/admin')
@login_required
def AdminPage():
    return render_template('admin.html')

@mbp.route('/account')
def AccountPage():
    return render_template('account.html')