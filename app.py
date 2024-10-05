from flask import Flask, jsonify, request
import mysql.connector

app = Flask(__name__)

# Configuración de la conexión a MySQL usando mysql.connector:
db = mysql.connector.connect(
    host="localhost",  
    user="root",
    password="password",  
    database="matricula"
)

# Crear un cursor global
cursor = db.cursor()

# Endpoint para obtener todos los registros de la tabla Dicta (GET):
@app.route('/dicta', methods=['GET'])
def get_dicta():
    cursor.execute("""
        SELECT d.id, p.nombres, d.codigo_curso, d.nombre_curso, d.seccion, d.periodo, d.cant_horas
        FROM Dicta d
        JOIN Profesor p ON d.id_profesor = p.id
    """)
    dicta_records = cursor.fetchall()
    result = []
    for row in dicta_records:
        result.append({
            'id': row[0],
            'profesor': row[1],
            'codigo_curso': row[2],
            'nombre_curso': row[3],
            'seccion': row[4],
            'periodo': row[5],
            'cant_horas': row[6] if row[6] is not None else 0
        })
    return jsonify(result)

# Endpoint para agregar un registro en la tabla Dicta (POST):
@app.route('/dicta', methods=['POST'])
def create_dicta():
    data = request.get_json()
    id_profesor = data.get('id_profesor')
    codigo_curso = data.get('codigo_curso')
    nombre_curso = data.get('nombre_curso')
    seccion = data.get('seccion')
    periodo = data.get('periodo')
    cant_horas = data.get('cant_horas', 0)

    query = """
    INSERT INTO Dicta (id_profesor, codigo_curso, nombre_curso, seccion, periodo, cant_horas)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    cursor.execute(query, (id_profesor, codigo_curso, nombre_curso, seccion, periodo, cant_horas))
    db.commit()

    return jsonify({'message': 'Dicta created successfully'}), 201

# Nuevo endpoint para agregar un Profesor (POST):
@app.route('/profesor', methods=['POST'])
def create_profesor():
    data = request.get_json()
    nombres = data.get('nombres')
    correo = data.get('correo')
    sueldo = data.get('sueldo')
    fecha_nacimiento = data.get('fecha_nacimiento')

    query = """
    INSERT INTO Profesor (nombres, correo, sueldo, fecha_nacimiento)
    VALUES (%s, %s, %s, %s)
    """
    cursor.execute(query, (nombres, correo, sueldo, fecha_nacimiento))
    db.commit()

    return jsonify({'message': 'Profesor created successfully'}), 201

# Ejecutando la aplicación:
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8005, debug=True)

