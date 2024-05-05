import sqlite3

# Conectar a la base de datos
conexion = sqlite3.connect("db/Inscripciones.db")
cursor = conexion.cursor()

# Ejecutar una consulta SQL para recuperar información de ambas tablas
consulta = """
           SELECT Cursos.*
           FROM Cursos
           INNER JOIN Inscritos
           ON Inscritos.Código_Curso = Cursos.Código_Curso
           WHERE No_Inscripción = 5"""

# Ejecutar la consulta con el ID específico
cursor.execute(consulta)
fila = cursor.fetchall()

query = """
        SELECT Cursos.* 
        FROM Cursos 
        LEFT JOIN Inscritos 
        ON Cursos.Código_Curso = Inscritos.Código_Curso and Inscritos.No_Inscripción = 18
        WHERE Inscritos.Código_Curso IS NULL ORDER BY Cursos.Código_Curso
        """
cursor.execute(query)
aui = cursor.fetchall()

# Mostrar los datos recuperados
print("Datos de la tabla principal:", fila)
print(aui)
# Cerrar la conexión a la base de datos
conexion.close()

import tkinter as tk
from tkinter import ttk

# Crear la ventana principal
root = tk.Tk()
root.geometry("300x200")

# Crear un estilo
estilo = ttk.Style()

# Configurar el estilo del Label
estilo.configure("MiEstilo.TLabel", background="lightblue", font=("Arial", 12))

# Crear un Label con el estilo personalizado
label = ttk.Label(root, text="Hola Mundo", style="MiEstilo.TLabel")

ttk.Style().configure("TButton", padding=6, relief="flat",
   background="#ccc")

btn = ttk.Button(text="Sample")
btn.pack()
label.pack(pady=20)

style = ttk.Style()
style.theme_settings("default", {
   "TCombobox": {
       "configure": {"padding": 5},
       "map": {
           "background": [("active", "green2"),
                          ("!disabled", "green4")],
           "fieldbackground": [("!disabled", "green3")],
           "foreground": [("focus", "OliveDrab1"),
                          ("!disabled", "OliveDrab2")]
       }
   }
})

combo = ttk.Combobox().pack()

root.mainloop()

