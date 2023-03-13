from flask import Blueprint
from flask import Flask, redirect, render_template
from flask import request
from flask import url_for
from models import Alumnos, db #ORM
import Alumnos.forms as forms

alumnos = Blueprint('alumnos',__name__)

@alumnos.route('/getAlum',methods = ['GET'])
def getAlum():
    return {'key':'Alumnos'}

@alumnos.route("/addAlum", methods = ['GET','POST'])
def index():
    create_form = forms.UserForm(request.form)
    if request.method == 'POST':
        alum = Alumnos(nombre = create_form.nombre.data,
                       apellidos = create_form.apellidos.data,
                       email = create_form.email.data)
        db.session.add(alum)
        db.session.commit()
        return redirect(url_for('alumnos.abc'))
    return render_template('index.html', form = create_form)

@alumnos.route("/abc", methods = ['GET','POST'])
def abc():
    abc_Form = forms.UserForm(request.form)
    alumno = Alumnos.query.all()

    return render_template('ABCompleto.html', form = abc_Form, alumno = alumno)

@alumnos.route("/modificar", methods = ['GET','POST'])
def modificar():
    mod_Form = forms.UserForm(request.form)

    if request.method == 'GET':
        id = request.args.get('id')
        alum1 = db.session.query(Alumnos).filter(Alumnos.id == id).first()
        mod_Form.id.data = request.args.get('id')
        mod_Form.nombre.data = alum1.nombre
        mod_Form.apellidos.data = alum1.apellidos
        mod_Form.email.data = alum1.email

    if request.method == 'POST':
        id = mod_Form.id.data
        alum = db.session.query(Alumnos).filter(Alumnos.id == id).first()
        alum.nombre = mod_Form.nombre.data
        alum.apellidos = mod_Form.apellidos.data
        alum.email = mod_Form.email.data
        
        db.session.add(alum)
        db.session.commit()
        return redirect(url_for('alumnos.abc'))
        
    return render_template('modificar.html',form = mod_Form)

@alumnos.route("/eliminar", methods = ['GET','POST'])
def eliminar():
    mod_Form = forms.UserForm(request.form)
    
    if request.method == 'GET':
        id = request.args.get('id')
        alum1 = db.session.query(Alumnos).filter(Alumnos.id == id).first()
        mod_Form.id.data = request.args.get('id')
        mod_Form.nombre.data = alum1.nombre
        mod_Form.apellidos.data = alum1.apellidos
        mod_Form.email.data = alum1.email

    if request.method == 'POST':
        id = mod_Form.id.data
        alum = db.session.query(Alumnos).filter(Alumnos.id == id).first()
        alum.nombre = mod_Form.nombre.data
        alum.apelidos = mod_Form.apellidos.data
        alum.email = mod_Form.email.data
        db.session.delete(alum)
        db.session.commit()
        return redirect(url_for('alumnos.abc'))
    return render_template('eliminar.html',form = mod_Form)