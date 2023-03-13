from flask import Blueprint
from flask import Flask, redirect, render_template
from flask import request
from flask import url_for
from models import Maestros, db  # ORM
import Maestros.forms as forms
from db import get_connection

maestros = Blueprint('maestros', __name__)


@maestros.route('/getM', methods=['GET'])
def getAlum():
    return {'key': 'Maestros'}


@maestros.route("/addMaes", methods=['GET', 'POST'])
def index():
    create_form = forms.UserForm(request.form)
    if request.method == 'POST':

        nombre = create_form.nombre.data
        apellidos = create_form.apellidos.data
        email = create_form.email.data
        materia = create_form.materia.data
        try:
            connection = get_connection()

            with connection.cursor() as cursor:
                cursor.execute('call insertarMaestros(%s,%s,%s,%s)',
                               (nombre, apellidos, email, materia))
                resultset = cursor.fetchall()

            connection.commit()
            connection.close()

            for row in resultset:
                print(row)
            return redirect(url_for('maestros.abcm'))
        except Exception as ex:
                print(ex)
    return render_template('maestros.html', form=create_form)


@maestros.route("/modificarM", methods=['GET', 'POST'])
def modificarM():
    mod_Form = forms.UserForm(request.form)
    
    if request.method == 'GET':
        id = request.args.get('id')
        maes1 = db.session.query(Maestros).filter(Maestros.id == id).first()
        mod_Form.id.data = request.args.get('id')
        mod_Form.nombre.data = maes1.nombre
        mod_Form.apellidos.data = maes1.apellidos
        mod_Form.email.data = maes1.email
        mod_Form.materia.data = maes1.materia
        
    if request.method == 'POST':
        id = mod_Form.id.data
        nombre = mod_Form.nombre.data
        apellidos = mod_Form.apellidos.data
        email = mod_Form.email.data
        materia = mod_Form.materia.data
        try:
            connection = get_connection()

            with connection.cursor() as cursor:
                cursor.execute('call actualizarMaestros(%s,%s,%s,%s,%s)',
                               (id, nombre, apellidos, email, materia))
                resultset = cursor.fetchall()
                
            connection.commit()
            connection.close()
                
            for row in resultset:
                print(row)
            return redirect(url_for('maestros.abcm'))
        except Exception as ex:
                print(ex)
        
    return render_template('modificarM.html',form = mod_Form)

@maestros.route("/eliminarM", methods=['GET', 'POST'])
def eliminarM():
    mod_Form = forms.UserForm(request.form)
    
    if request.method == 'GET':
        id = request.args.get('id')
        maes1 = db.session.query(Maestros).filter(Maestros.id == id).first()
        mod_Form.id.data = request.args.get('id')
        mod_Form.nombre.data = maes1.nombre
        mod_Form.apellidos.data = maes1.apellidos
        mod_Form.email.data = maes1.email
        mod_Form.materia.data = maes1.materia
        
    if request.method == 'POST':
        id = mod_Form.id.data
        try:
            connection = get_connection()

            with connection.cursor() as cursor:
                cursor.execute('call eliminarMaestros(%s)',
                               (id))
                resultset = cursor.fetchall()
                
            connection.commit()
            connection.close()
                
            for row in resultset:
                print(row)
            return redirect(url_for('maestros.abcm'))
        except Exception as ex:
                print(ex)
        
    return render_template('eliminarM.html',form = mod_Form)

@maestros.route("/abcm", methods = ['GET','POST'])
def abcm():
    abc_Form = forms.UserForm(request.form)
    mt = Maestros.query.all()

    return render_template('ABCompletoM.html', form = abc_Form, maestro = mt)
