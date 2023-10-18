from gta import create_app
from flask_bootstrap import Bootstrap5

app = create_app()
bootstrap = Bootstrap5(app)
app.app_context().push()

if __name__=="__main__":
    app.run()