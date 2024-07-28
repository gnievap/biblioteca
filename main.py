import os

import psycopg2
from flask import Flask, request, redirect, render_template, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms.fields import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired

import db
from forms import LibrosForm

app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config['SECRET_KEY'] = 'SUPER SECRETO'

@app.route('/')
def index():
    return render_template('base.html')

@app.errorhandler(404)
def error404(error):
    return render_template('404.html')

@app.route('/libros')
def libros():
    conn = db.conectar()
    # crear un cursor (objeto para recorrer las tablas)
    cursor = conn.cursor()
    # ejecutar una consulta en postgres
    cursor.execute('''SELECT * FROM libros_view''')
    #recuperar la informacion
    datos = cursor.fetchall()
    #cerrar cursos y conexion a la base de datos
    cursor.close()
    db.desconectar(conn)
    return render_template('libros.html', datos=datos)

@app.route('/insertar_libro', methods=['GET', 'POST'])
def insertar_libro():
    form = LibrosForm()

    autores = obtener_autores()
    form.fk_autor.choices = [(autor[0], f"{autor[1]} {autor[2]}") for autor in autores]
    editoriales = obtener_editoriales()
    form.fk_editorial.choices = [(editorial[0], f"{editorial[1]}") for editorial in editoriales]

    if form.validate_on_submit():
        # Si se dió click en el botón del form y no faltan datos
        # se recupera la información que el user escribió en el form
        titulo = form.titulo.data
        fk_autor = form.fk_autor.data
        fk_editorial = form.fk_editorial.data
        edicion = form.edicion.data
        # Insertar los datos
        conn = db.conectar()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO libro (titulo, fk_autor, fk_editorial, edicion)
                       VALUES (%s, %s, %s, %s)''', (titulo, fk_autor, fk_editorial, edicion))
        conn.commit()
        cursor.close()
        db.desconectar(conn)
        return redirect(url_for('libros'))
    return render_template('insertar_libro.html', form=form)

# Buscar el id, nombre y apellido de los autores
def obtener_autores():
    conn = db.conectar()
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM autor''')
    autores = cursor.fetchall() 
    # Crear una lista de diccionarios con los campos deseados
    lista_autores = []
    for autor in autores:
        autor_dict = {
            'id': autor[0],
            'nombre': autor[2],
            'apellido': autor[3]
        }
        lista_autores.append(autor_dict)
    cursor.close()
    db.desconectar(conn)
    return autores

# Buscar el id y nombre de las editoriales
def obtener_editoriales():
    conn = db.conectar()
    cursor = conn.cursor()
    cursor.execute('''SELECT id_editorial, nombre FROM editorial''')
    editoriales = cursor.fetchall() 
    # Crear una lista de diccionarios con los campos deseados
    lista_editoriales = []
    for editorial in editoriales:
        editorial_dict = {
            'id': editorial[0],
            'nombre': editorial[1],
        }
        lista_editoriales.append(editorial_dict)
    cursor.close()
    db.desconectar(conn)
    return editoriales

@app.route('/autores')
def autores():
    conn = db.conectar()
    # crear un cursor (objeto para recorrer las tablas)
    cursor = conn.cursor()
    # ejecutar una consulta en postgres
    cursor.execute('''SELECT * FROM autores_view''')
    #recuperar la informacion
    datos = cursor.fetchall()
    #cerrar cursos y conexion a la base de datos
    cursor.close()
    db.desconectar(conn)
    return render_template('autores.html', datos=datos)

@app.route('/paises')
def paises():
    conn = db.conectar()
    # crear un cursor (objeto para recorrer las tablas)
    cursor = conn.cursor()
    # ejecutar una consulta en postgres
    cursor.execute('''SELECT * FROM pais ORDER BY id_pais''')
    #recuperar la informacion
    datos = cursor.fetchall()
    #cerrar cursos y conexion a la base de datos
    cursor.close()
    db.desconectar(conn)
    return render_template('paises.html', datos=datos)

@app.route('/delete_pais/<int:id_pais>', methods=['POST'])
def delete_pais(id_pais):
    conn = db.conectar()
    # crear un cursor (objeto para recorrer las tablas)
    cursor = conn.cursor()
    # Borrar el registro con el id_pais seleccionado
    cursor.execute('''DELETE FROM pais WHERE id_pais=%s''',
                   (id_pais,))
    conn.commit()
    cursor.close()
    db.desconectar(conn)
    return redirect(url_for('index'))

@app.route('/update1_pais/<int:id_pais>', methods=['POST'])
def update1_pais(id_pais):
    conn = db.conectar()
    # crear un cursor (objeto para recorrer las tablas)
    cursor = conn.cursor()
    # recuperar el registro del id_pais seleccionado
    cursor.execute('''SELECT * FROM pais WHERE id_pais=%s''',
                   (id_pais,))
    datos = cursor.fetchall()
    cursor.close()
    db.desconectar(conn)
    return render_template('editar_pais.html', datos=datos)

@app.route('/update2_pais/<int:id_pais>', methods=['POST'])
def update2_pais(id_pais):
    nombre = request.form['nombre']
    conn = db.conectar()
    # crear un cursor (objeto para recorrer las tablas)
    cursor = conn.cursor()
    cursor.execute('''UPDATE pais SET nombre=%s WHERE id_pais=%s''', (nombre, id_pais,))
    conn.commit()
    cursor.close()
    db.desconectar(conn)
    return redirect(url_for('index'))