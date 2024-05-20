import sqlite3

def insertar_datos(carreras):
    # Conectar a la base de datos
    conn = sqlite3.connect('db/Inscripciones.db')
    cursor = conn.cursor()

    # Insertar datos en la tabla
    cursor.executemany('''
    INSERT INTO Alumnos (Id_Alumno, Id_Carrera, Nombres, Apellidos, Fecha_Ingreso, Ciudad, Departamento)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', carreras)

    # Confirmar los cambios y cerrar la conexión
    conn.commit()
    conn.close()



# Insertar datos en la base de datos
import random
from datetime import datetime, timedelta

# Códigos de las carreras
codigos_carreras = ["C001", "C002", "C003", "C004", "C005", "C006", "C007", "C008", "C009", "C010", "C011", "C012", "C013", "C014", "C015", "C016", "C017", "C018", "C019", "C020", "C021", "C022", "C023", "C024", "C025", "C026", "C027", "C028", "C029", "C030", "C031", "C032", "C033", "C034", "C035", "C036", "C037", "C038", "C039", "C040", "C041", "C042", "C043"]

# Sedes de la Universidad Nacional de Colombia
sedes = [
    ("Bogotá", "Bogotá D.C."),
    ("Medellín", "Antioquia"),
    ("Manizales", "Caldas"),
    ("Palmira", "Valle del Cauca"),
    ("Amazonia", "Amazonas"),
    ("Caribe", "San Andrés y Providencia"),
    ("Orinoquia", "Arauca"),
    ("Tumaco", "Nariño")
]

# Listas de nombres y apellidos
nombres = [
    "Daniel", "Mateo", "Santiago", "Valentina", "Sofía", "Mariana", "Lucas", "Martín", "Camila", "Lucía",
    "Alejandro", "Miguel", "Juan", "Isabella", "Gabriela", "Samuel", "Diana", "Laura", "Carlos", "Andrés",
    "Sebastián", "Emilio", "Tomás", "Catalina", "Antonia", "Elena", "Gabriel", "Luis", "Fernando", "Javier",
    "Manuel", "Francisco", "David", "Jorge", "Ángel", "Diego", "Leonardo", "Victoria", "Paula", "Ana",
    "Andrea", "María", "Carolina", "Natalia", "José", "Iván", "Ricardo", "Álvaro", "Eduardo", "Felipe"
]

apellidos = [
    "González", "Rodríguez", "Gómez", "Fernández", "López", "Díaz", "Martínez", "Pérez", "García", "Sánchez",
    "Romero", "Alvarez", "Torres", "Ruiz", "Ramírez", "Flores", "Acosta", "Castillo", "Ortega", "Gutiérrez",
    "Vargas", "Molina", "Morales", "Silva", "Rojas", "Ortiz", "Medina", "Cruz", "Reyes", "Jiménez",
    "Herrera", "Guzmán", "Pacheco", "Navarro", "Rivera", "Espinosa", "Soto", "Ramos", "Suárez", "Chávez",
    "Román", "Vega", "Montoya", "Villalobos", "Campos", "Carrillo", "Salazar", "Aguilar", "Bautista", "Delgado"
]

# Generar fechas de ingreso aleatorias entre 01/01/2016 y 31/12/2023
def generar_fecha_ingreso():
    start_date = datetime.strptime('01/01/2016', '%d/%m/%Y')
    end_date = datetime.strptime('31/12/2023', '%d/%m/%Y')
    delta = end_date - start_date
    random_days = random.randint(0, delta.days)
    fecha_ingreso = start_date + timedelta(days=random_days)
    return fecha_ingreso.strftime('%d/%m/%Y')

# Generar lista de alumnos
alumnos = []
for i in range(1, 101):
    id_alumno = 100000 + i*500 + random.randint(1, 100)
    codigo_carrera = random.choice(codigos_carreras)
    nombre = random.choice(nombres)+" "+random.choice(nombres)
    apellido = random.choice(apellidos)+" "+random.choice(apellidos)
    fecha_ingreso = generar_fecha_ingreso()
    ciudad, departamento = random.choice(sedes)
    alumno = (id_alumno, codigo_carrera, nombre, apellido, fecha_ingreso, ciudad, departamento)
    alumnos.append(alumno)

insertar_datos(alumnos)

# Leer y mostrar los datos almacenados

