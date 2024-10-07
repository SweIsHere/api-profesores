from flask import Flask, jsonify, request
import mysql.connector

app = Flask(__name__)

# Configuración de la conexión a MySQL
db = mysql.connector.connect(
    host="52.45.141.206",
    user="root",
    password="utec",
    database="matricula",
    port=8005
)

# Crear un cursor global
cursor = db.cursor()


### CRUD para la tabla "Profesor" ###


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











@app.route('/dicta/<int:dicta_id>/profesor/<int:profesor_id>', methods=['POST'])
def assign_profesor_to_dicta(dicta_id, profesor_id):
    try:
        # Verificar que el registro de Dicta existe
        cursor.execute("SELECT * FROM Dicta WHERE id = %s", (dicta_id,))
        dicta_record = cursor.fetchone()
        if not dicta_record:
            return jsonify({'message': 'Dicta not found'}), 404

        # Verificar que el profesor existe
        cursor.execute("SELECT * FROM Profesor WHERE id = %s", (profesor_id,))
        profesor_record = cursor.fetchone()
        if not profesor_record:
            return jsonify({'message': 'Profesor not found'}), 404

        # Asociar el profesor al registro de Dicta
        cursor.execute("""
            UPDATE Dicta SET id_profesor = %s WHERE id = %s
        """, (profesor_id, dicta_id))
        db.commit()

        return jsonify({'message': 'Profesor assigned to Dicta successfully'}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/dicta/<int:dicta_id>/profesor', methods=['DELETE'])
def remove_profesor_from_dicta(dicta_id):
    try:
        # Verificar que el registro de Dicta existe
        cursor.execute("SELECT * FROM Dicta WHERE id = %s", (dicta_id,))
        dicta_record = cursor.fetchone()
        if not dicta_record:
            return jsonify({'message': 'Dicta not found'}), 404

        # Remover la relación con el profesor
        cursor.execute("""
            UPDATE Dicta SET id_profesor = NULL WHERE id = %s
        """, (dicta_id,))
        db.commit()

        return jsonify({'message': 'Profesor removed from Dicta successfully'}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500








@app.route('/profesor', methods=['GET'])
def get_profesores():
    try:
        cursor.execute("SELECT * FROM Profesor")
        profesores = cursor.fetchall()
        result = []
        for row in profesores:
            result.append({
                'id': row[0],
                'nombres': row[1],
                'correo': row[2],
                'sueldo': row[3],
                'fecha_nacimiento': str(row[4])
            })
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/profesor/<int:id>', methods=['GET'])
def get_profesor(id):
    try:
        cursor.execute("SELECT * FROM Profesor WHERE id = %s", (id,))
        profesor = cursor.fetchone()
        if profesor:
            result = {
                'id': profesor[0],
                'nombres': profesor[1],
                'correo': profesor[2],
                'sueldo': profesor[3],
                'fecha_nacimiento': str(profesor[4])
            }
            return jsonify(result), 200
        return jsonify({'message': 'Profesor not found'}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500



@app.route('/profesor/correo/<string:correo>', methods=['GET'])
def get_profesor_by_correo(correo):
    try:
        cursor.execute("SELECT * FROM Profesor WHERE correo = %s", (correo,))
        profesor = cursor.fetchone()
        if profesor:
            result = {
                'id': profesor[0],
                'nombres': profesor[1],
                'correo': profesor[2],
                'sueldo': profesor[3],
                'fecha_nacimiento': str(profesor[4])
            }
            return jsonify(result), 200
        return jsonify({'message': 'Profesor not found'}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/profesor', methods=['POST'])
def create_profesor():
    try:
        data = request.get_json()

        # Validar que todos los campos requeridos están presentes
        if not data or not all(key in data for key in ('nombres', 'correo', 'sueldo', 'fecha_nacimiento')):
            return jsonify({"error": "All fields (nombres, correo, sueldo, fecha_nacimiento) are required"}), 400

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
    except Exception as e:
        return jsonify({"error": str(e)}), 500




@app.route('/profesor/<int:id>', methods=['PUT'])
def update_profesor(id):
    try:
        data = request.get_json()

        # Validar que todos los campos requeridos están presentes
        if not data or not all(key in data for key in ('nombres', 'correo', 'sueldo', 'fecha_nacimiento')):
            return jsonify({"error": "All fields (nombres, correo, sueldo, fecha_nacimiento) are required"}), 400

        nombres = data.get('nombres')
        correo = data.get('correo')
        sueldo = data.get('sueldo')
        fecha_nacimiento = data.get('fecha_nacimiento')

        query = """
        UPDATE Profesor SET nombres=%s, correo=%s, sueldo=%s, fecha_nacimiento=%s WHERE id=%s
        """
        cursor.execute(query, (nombres, correo, sueldo, fecha_nacimiento, id))
        db.commit()

        return jsonify({'message': 'Profesor updated successfully'}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/profesor/<int:id>', methods=['PATCH'])
def patch_profesor(id):
    try:
        data = request.get_json()

        # Validar que haya al menos un campo para actualizar
        if not data:
            return jsonify({"error": "No data provided"}), 400

        update_fields = []
        update_values = []

        for field in ['nombres', 'correo', 'sueldo', 'fecha_nacimiento']:
            if field in data:
                update_fields.append(f"{field}=%s")
                update_values.append(data[field])

        if not update_fields:
            return jsonify({"error": "No valid fields to update"}), 400

        update_values.append(id)
        query = f"UPDATE Profesor SET {', '.join(update_fields)} WHERE id=%s"
        cursor.execute(query, update_values)
        db.commit()

        return jsonify({'message': 'Profesor partially updated successfully'}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500



@app.route('/profesor/<int:id>', methods=['DELETE'])
def delete_profesor(id):
    try:
        cursor.execute("DELETE FROM Profesor WHERE id=%s", (id,))
        db.commit()
        return jsonify({'message': 'Profesor deleted successfully'}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500




@app.route('/dicta/<int:id>', methods=['GET'])
def get_dicta_by_id(id):
    try:
        cursor.execute("""
            SELECT d.id, p.nombres, d.codigo_curso, d.nombre_curso, d.seccion, d.periodo, d.cant_horas
            FROM Dicta d
            JOIN Profesor p ON d.id_profesor = p.id
            WHERE d.id = %s
        """, (id,))
        dicta_record = cursor.fetchone()
        if dicta_record:
            result = {
                'id': dicta_record[0],
                'profesor': dicta_record[1],
                'codigo_curso': dicta_record[2],
                'nombre_curso': dicta_record[3],
                'seccion': dicta_record[4],
                'periodo': dicta_record[5],
                'cant_horas': dicta_record[6] if dicta_record[6] is not None else 0
            }
            return jsonify(result), 200
        return jsonify({'message': 'Dicta record not found'}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/dicta', methods=['POST'])
def create_dicta():
    try:
        data = request.get_json()

        # Validar que todos los campos requeridos están presentes
        if not data or not all(key in data for key in ('id_profesor', 'codigo_curso', 'nombre_curso', 'seccion', 'periodo')):
            return jsonify({"error": "All fields are required"}), 400

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
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/dicta/<int:id>', methods=['PUT'])
def update_dicta(id):
    try:
        data = request.get_json()

        # Validar que todos los campos requeridos están presentes
        if not data or not all(key in data for key in ('id_profesor', 'codigo_curso', 'nombre_curso', 'seccion', 'periodo')):
            return jsonify({"error": "All fields are required"}), 400

        id_profesor = data.get('id_profesor')
        codigo_curso = data.get('codigo_curso')
        nombre_curso = data.get('nombre_curso')
        seccion = data.get('seccion')
        periodo = data.get('periodo')
        cant_horas = data.get('cant_horas')

        query = """
        UPDATE Dicta SET id_profesor=%s, codigo_curso=%s, nombre_curso=%s, seccion=%s, periodo=%s, cant_horas=%s WHERE id=%s
        """
        cursor.execute(query, (id_profesor, codigo_curso, nombre_curso, seccion, periodo, cant_horas, id))
        db.commit()

        return jsonify({'message': 'Dicta updated successfully'}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/dicta/<int:id>', methods=['DELETE'])
def delete_dicta(id):
    try:
        cursor.execute("DELETE FROM Dicta WHERE id=%s", (id,))
        db.commit()
        return jsonify({'message': 'Dicta deleted successfully'}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Ejecutar la aplicación Flask
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8005, debug=True)