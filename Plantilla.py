# !/usr/bin/python3
# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import messagebox as msg
import tkinter.ttk as ttk
import sqlite3 as sql
from datetime import datetime

class Inscripciones:
    
    def __init__(self, master=None):
        # Ventan principal    
        
        self.win = tk.Tk(master)
        self.win.configure(background="#f7f9fd") #fondo ventana
        wwin, hwin = 800, 600 #Tamaño de la ventana
        px = round(self.win.winfo_screenwidth()/2-wwin/2) # posición x
        py = round(self.win.winfo_screenheight()/2-hwin/2) # posición y
        self.win.geometry(str(wwin)+"x"+str(hwin)+"+"+str(px)+"+"+str(py))#posición y tamaño de la ventana
        self.win.resizable(False, False)
        self.win.title("Inscripciones de Materias y Cursos")
        self.win.iconbitmap( "img/icono2.ico")
        
        # Crea los frames
        self.frm_1 = tk.Frame(self.win, name="frm_1")
        self.frm_1.configure(background="#f7f9fd", height=600, width=800)
        self.lblNoInscripcion = ttk.Label(self.frm_1, name="lblnoinscripcion")
        self.lblNoInscripcion.configure(background="#f7f9fd",font="{Arial} 11 {bold}",
                                        justify="left",state="normal",
                                        takefocus=False,text='No.Inscripción')
        
        #Label No. Inscripción
        self.lblNoInscripcion.place(anchor="nw", x=680, y=20)
        
        #Entry No. Inscripción
        self.num_Inscripcion = ttk.Entry(self.frm_1, name="num_inscripcion")
        self.num_Inscripcion.configure(justify="right")
        self.num_Inscripcion.place(anchor="nw", width=100, x=682, y=42)
        
        #Label Fecha
        self.lblFecha = ttk.Label(self.frm_1, name="lblfecha")
        self.lblFecha.configure(background="#f7f9fd", text='Fecha:')
        self.lblFecha.place(anchor="nw", x=630, y=80)
        
        #Entry Fecha
        self.fecha = ttk.Entry(self.frm_1, name="fecha")
        self.fecha.configure(justify="center")
        self.fecha.place(anchor="nw", width=90, x=680, y=80)
        self.fecha.insert(0,"dd/mm/aaaa") #formato fecha
        #borrar formato cuando se pose encima del entry
        self.fecha.bind("<FocusIn>",lambda event: self.fecha.delete(0, tk.END) if self.fecha.get()=="dd/mm/aaaa" else None) 
        #verificar la fecha si sale del entry o si esta vacio, mostrar el formato de la fecha
        self.fecha.bind("<FocusOut>",lambda event: self.fecha.insert(0, "dd/mm/aaaa") if self.fecha.get()=="" else self.val_fecha())
        self.fecha.bind("<KeyRelease>",self.validacion_size_fecha)
        
        
        #Label ID Alumno
        self.lblIdAlumno = ttk.Label(self.frm_1, name="lblidalumno")
        self.lblIdAlumno.configure(background="#f7f9fd", text='Id Alumno:')
        self.lblIdAlumno.place(anchor="nw", x=30, y=85)
        
        #Combobox Alumno
        self.idAlumSelect=tk.StringVar()
        self.cmbx_Id_Alumno = ttk.Combobox(self.frm_1,state="readonly", 
                                           name="cmbx_id_alumno", 
                                           postcommand=self.update_arrow_IdAlum , 
                                           textvariable=self.idAlumSelect)
        self.cmbx_Id_Alumno.place(anchor="nw", width=112, x=110, y=85)
        self.cmbx_Id_Alumno.bind('<<ComboboxSelected>>', self.infoAlum)

        #Label Alumno
        self.lblNombres = ttk.Label(self.frm_1, name="lblnombres")
        self.lblNombres.configure(background="#f7f9fd",text='Nombre(s):')
        self.lblNombres.place(anchor="nw", x=30, y=140)
       
        
        #Entry Alumno
        self.nombres = ttk.Entry(self.frm_1, name="nombres",state="readonly")
        self.nombres.place(anchor="nw", width=200, x=110, y=140)
        
        #Label Apellidos
        self.lblApellidos = ttk.Label(self.frm_1, name="lblapellidos")
        self.lblApellidos.configure(text='Apellido(s):')
        self.lblApellidos.place(anchor="nw", x=400, y=140)
        
        #Entry Apellidos
        self.apellidos = ttk.Entry(self.frm_1, name="apellidos",state="readonly")
        self.apellidos.place(anchor="nw", width=200, x=485, y=140)

        ''' Botones  de la Aplicación'''
        
        #Botón Guardar
        self.btnGuardar = ttk.Button(self.frm_1, name="btnguardar")
        self.btnGuardar.configure(text='Guardar')
        self.btnGuardar.place(anchor="nw", x=200, y=220)
        
        #Botón Editar
        self.btnEditar = ttk.Button(self.frm_1, name="btneditar")
        self.btnEditar.configure(text='Editar')
        self.btnEditar.place(anchor="nw", x=300, y=220)
        
        #Botón Eliminar
        self.btnEliminar = ttk.Button(self.frm_1, name="btneliminar")
        self.btnEliminar.configure(text='Eliminar')
        self.btnEliminar.place(anchor="nw", x=400, y=220)
        
        #Botón Cancelar
        self.btnCancelar = ttk.Button(self.frm_1, name="btncancelar")
        self.btnCancelar.configure(text='Cancelar')
        self.btnCancelar.place(anchor="nw", x=500, y=220)
        
        #Separador
        separator1 = ttk.Separator(self.frm_1)
        separator1.configure(orient="horizontal")
        separator1.place(anchor="nw", width=796, x=2, y=260)

        ''' Treeview de la Aplicación'''
        
        #Treeview
        self.tView = ttk.Treeview(self.frm_1, name="tview")
        self.tView.configure(selectmode="extended")
        
        #Columnas del Treeview
        self.tView_cols = ['tV_descripción']
        self.tView_dcols = ['tV_descripción']
        self.tView.configure(columns=self.tView_cols,displaycolumns=self.tView_dcols)
        self.tView.column("#0",anchor="w",stretch=True,width=10,minwidth=10)
        self.tView.column("tV_descripción",anchor="w",stretch=True,width=200,minwidth=50)
        
        #Cabeceras
        self.tView.heading("#0", anchor="w", text='Curso')
        self.tView.heading("tV_descripción", anchor="w", text='Descripción')
        self.tView.place(anchor="nw", height=300, width=790, x=4, y=280)
        
        #Scrollbars
        self.scroll_H = ttk.Scrollbar(self.tView,name="scroll_h")
        self.scroll_H.configure(orient="horizontal")
        self.scroll_H.place(anchor="s", height=12, width=1534, x=15, y=595)
        self.scroll_Y = ttk.Scrollbar(self.tView, name="scroll_y")
        self.scroll_Y.configure(orient="vertical")
        self.scroll_Y.place(anchor="s", height=275, width=12, x=790, y=582)
        self.frm_1.pack(side="top")
        self.frm_1.pack_propagate(0)

        # Main widget
        self.mainwindow = self.win

    def run(self):
        self.mainwindow.mainloop()
        

    ''' A partir de este punto se deben incluir las funciones
     para el manejo de la base de datos '''
     
    #validación tamaño fecha
    def validacion_size_fecha(self, event):
        
        #insertar "/"" automatico para separar dias, mese y años
        if len(self.fecha.get())==2 or len(self.fecha.get())==5:
            self.fecha.insert(tk.END,"/")
            
        #Verificación de maximo de caracteres permitidos en fecha
        elif len(self.fecha.get())>10:
            msg.showerror(title="¡Atención!",
                         message="-Maximo 10 caracteres-"
                   )
            self.fecha.delete(10, tk.END) #borrar caracteres demas
            
    #Verificar si la fecha digitada es valida
    def val_fecha(self):
        
        if len(self.fecha.get())<=10:
            try:
             # Intentar convertirla a una fecha.
                fechav = datetime.strptime(self.fecha.get(), "%d/%m/%Y")
            except:
                msg.showerror(title="¡Atención!",
                         message="Fecha no valida"
                   )
    
    #Extraer datos de alumnos de la db de forma dinamica
    def update_arrow_IdAlum(self, *args):
        
        conn = sql.connect("db/Inscripciones.db")
        cursor = conn.cursor()
        instrc = f"SELECT Id_Alumno FROM Alumnos ORDER BY Id_Alumno"
        cursor.execute(instrc)
        datos =cursor.fetchall()
        self.cmbx_Id_Alumno['values']=datos
        conn.close()
                
    def infoAlum(self,event):
        
        #Hacer modificables los entry
        self.apellidos.config(state="normal") 
        self.nombres.config(state="normal")
        #eliminar si hay residuos en los campos
        self.nombres.delete(0,tk.END)
        self.apellidos.delete(0,tk.END) 
        conn = sql.connect("db/Inscripciones.db")
        cursor = conn.cursor()
        instrc = f"SELECT Nombres, Apellidos FROM Alumnos WHERE Id_Alumno='{self.idAlumSelect.get()}'"
        cursor.execute(instrc)
        datos =cursor.fetchall() # se retorna una tupla de listas
        conn.commit()
        conn.close()
        #Insertar en los entrys nombres y apellidos
        self.nombres.insert(0,datos[0][0])
        self.apellidos.insert(0,datos[0][1])
        #Volver a dejar el entry como "solo lectura"
        self.apellidos.config(state="readonly")
        self.nombres.config(state="readonly")
    
if __name__ == "__main__":
    app = Inscripciones()
    app.run()
