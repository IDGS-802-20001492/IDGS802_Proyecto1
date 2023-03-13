from flask import Flask, redirect, render_template
from flask import request
from flask import url_for
from config import DevelopmentConfig
from Alumnos.routes import alumnos
from Maestros.routes import maestros
from flask_wtf.csrf import CSRFProtect
from models import Alumnos, db #ORM
import Alumnos.forms as forms
app = Flask(__name__)

app.config['DEBUG'] = True
app.config.from_object(DevelopmentConfig)

@app.route("/", methods = ['GET','POST'])
def index():
    return render_template("home.html")

app.register_blueprint(alumnos)
app.register_blueprint(maestros)


csrf = CSRFProtect()

if __name__ == '__main__':
    csrf.init_app(app)
    db.init_app(app)
    with app.app_context():
        db.create_all #Se borró los ()
    app.run(port=3000)