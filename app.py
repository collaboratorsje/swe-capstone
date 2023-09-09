from flask import Flask, render_template
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'dev'
bootstrap = Bootstrap5(app)
db = SQLAlchemy()
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["FLASK_ENV"] = "development"
app.config["DEBUG"] = True
db.init_app(app)

@app.route('/')
def Home():
    return render_template("index.html")

if __name__ == '__main__':
    app.run()