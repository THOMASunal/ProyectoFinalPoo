import tkinter as tk
from tkinter import ttk

def cabecera_seleccionada(event):
    # Identificar la columna seleccionada
    current_item_id = tree.focus()
    current_item = tree.item(current_item_id)
    lista=current_item["values"]
    # Obtener el texto del encabezado de la columna
    print("Cabecera seleccionada:", current_item["text"],type(lista))

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