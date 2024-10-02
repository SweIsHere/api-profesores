from flask import Flask, jsonify, request
import MySQLdb

app = Flask(__name__)

# Configuración de la conexión a MySQL
db = MySQLdb.connect(
    host="localhost",  
    user="root",
    passwd="password", 
    db="matricula"
)

# Obteniendo todos los registros de "Dicta"
@app.route('/dicta', methods=['GET'])
def get_dicta():
    cursor = db.cursor()
    cursor.execute("""
        SELECT d.id, p.nombres, d.codigo_curso, d.nombre_curso, d.seccion, d.periodo, d.cant_horas
        FROM Dicta d
        JOIN Profesor p ON d.id_profesor = p.id
    """)
    dicta = cursor.fetchall()
    resultado = []
    for item in dicta:
        resultado.append({
            'id': item[0],
            'profesor': item[1],
            'codigo_curso': item[2],
            'nombre_curso': item[3],
            'seccion': item[4],
            'periodo': item[5],
            'cant_horas': item[6]
        })
    return jsonify(resultado)

# Añadiendo un nuevo registro a "Dicta"
@app.route('/dicta', methods=['POST'])
def add_dicta():
    nuevo_dicta = request.json
    cursor = db.cursor()
    cursor.execute("""
        INSERT INTO Dicta (id_profesor, codigo_curso, nombre_curso, seccion, periodo, cant_horas)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (nuevo_dicta['id_profesor'], nuevo_dicta['codigo_curso'], nuevo_dicta['nombre_curso'], 
          nuevo_dicta['seccion'], nuevo_dicta['periodo'], nuevo_dicta.get('cant_horas')))
    db.commit()
    return jsonify({'mensaje': 'Dicta agregado correctamente'}), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8005)
