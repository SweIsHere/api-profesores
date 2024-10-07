CREATE DATABASE matricula;

USE matricula;

CREATE TABLE Profesor (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombres VARCHAR(100),
    correo VARCHAR(100),
    sueldo DECIMAL(10, 2),
    fecha_nacimiento DATE
);

CREATE TABLE Dicta (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_profesor INT,
    codigo_curso VARCHAR(10),
    nombre_curso VARCHAR(100),
    seccion INT,
    periodo VARCHAR(10),
    cant_horas INT,
    FOREIGN KEY (id_profesor) REFERENCES Profesor(id)
);

-- Datos de ejemplo:
INSERT INTO Profesor (id, nombres, correo, sueldo, fecha_nacimiento) 
VALUES (1, 'Geraldo', 'colchado@utec', 3500.00, '1980-05-10');

INSERT INTO Dicta (id_profesor, codigo_curso, nombre_curso, seccion, periodo, cant_horas) 
VALUES (1, 'CS2031', 'Cloud Computing', 1, '2024-2', 12);
