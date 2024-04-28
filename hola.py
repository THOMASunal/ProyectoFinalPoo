import tkinter as tk
from tkinter import ttk

def cabecera_seleccionada(event):
    # Identificar la columna seleccionada
    columna_id = tree.identify_column(event.x)
    fila_id= tree.identify_region(y=event.y,x=event.x)
    # Obtener el texto del encabezado de la columna
    print("Cabecera seleccionada:", columna_id, fila_id,type(fila_id))

# Crear la ventana principal
root = tk.Tk()
root.title("TreeView con cabecera seleccionable")

# Crear el TreeView
tree = ttk.Treeview(root, columns=("Columna1", "Columna2", "Columna3"))

# Agregar datos de ejemplo
for i in range(10):
    tree.insert("", "end", values=("Dato1", "Dato2", "Dato3"))

# Configurar encabezados de columnas
tree.heading("#0", text="ID")
tree.heading("Columna1", text="Cabecera 1")
tree.heading("Columna2", text="Cabecera 2")
tree.heading("Columna3", text="Cabecera 3")

# Asociar la función de devolución de llamada al evento de clic en la cabecera
tree.bind("<Button-1>", cabecera_seleccionada)

# Empaquetar el TreeView
tree.pack(expand=True, fill="both")

# Ejecutar el bucle principal de la aplicación
root.mainloop()