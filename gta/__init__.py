from flask import Flask
from config import Config
from gta.extensions import db, login_manager

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    with app.app_context():
        db.init_app(app)
        login_manager.init_app(app)
        login_manager.login_view = "form.LoginPage"
        from gta.main import bp as mbp
        app.register_blueprint(mbp)
        from gta.form import bp as fbp
        app.register_blueprint(fbp)
        from gta.model import bp as mobp
        app.register_blueprint(mobp)
    @app.route('/test/')
    def test_page():
        return '<h1>Testing the Flask Application Factory Pattern</h1>'
    return app
