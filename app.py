from flask import Flask, jsonify, request
import MySQLdb

app = Flask(_name_)

# Configuración de la conexión a MySQL
db = MySQLdb.connect(
    host="localhost", 
    user="root",
    passwd="password", 
    db="matricula"
)

@app.route('/profesores', methods=['GET'])
def get_profesores():
    cursor = db.cursor()
    cursor.execute("SELECT * FROM Profesor")
    profesores = cursor.fetchall()
    resultado = []
    for profesor in profesores:
        resultado.append({
            'id': profesor[0],
            'nombre': profesor[1],
            'correo': profesor[2]
        })
    return jsonify(resultado)

@app.route('/profesores', methods=['POST'])
def add_profesor():
    nuevo_profesor = request.json
    cursor = db.cursor()
    cursor.execute("INSERT INTO Profesor (id, nombre, correo) VALUES (%s, %s, %s)",
                   (nuevo_profesor['id'], nuevo_profesor['nombre'], nuevo_profesor['correo']))
    db.commit()
    return jsonify({'mensaje': 'Profesor agregado'}), 201

@app.route('/cursos', methods=['GET'])
def get_cursos():
    cursor = db.cursor()
    cursor.execute("SELECT * FROM Curso")
    cursos = cursor.fetchall()
    resultado = []
    for curso in cursos:
        resultado.append({
            'id': curso[0],
            'nombre': curso[1],
            'creditos': curso[2]
        })
    return jsonify(resultado)

@app.route('/cursos', methods=['POST'])
def add_curso():
    nuevo_curso = request.json
    cursor = db.cursor()
    cursor.execute("INSERT INTO Curso (id, nombre, creditos) VALUES (%s, %s, %s)",
                   (nuevo_curso['id'], nuevo_curso['nombre'], nuevo_curso['creditos']))
    db.commit()
    return jsonify({'mensaje': 'Curso agregado'}), 201

if _name_ == '_main_':
    app.run(host='0.0.0.0', port=8005)