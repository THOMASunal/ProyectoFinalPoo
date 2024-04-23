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
           
        self.db_name = "db/Inscripciones.db" #establecer la ruta de la db
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
        self.lblIdAlumno.place(anchor="nw", x=20, y=85)
        
        #Combobox Alumno
        self.idAlumSelect=tk.StringVar()
        self.cmbx_Id_Alumno = ttk.Combobox(self.frm_1,
                                           name="cmbx_id_alumno", 
                                           postcommand=self.update_arrow_IdAlum , 
                                           textvariable=self.idAlumSelect)
        self.cmbx_Id_Alumno.place(anchor="nw", width=112, x=110, y=85)
        self.cmbx_Id_Alumno.bind("<<ComboboxSelected>>", self.info_Alum)
        #self.cmbx_Id_Alumno.bind("<KeyRelease>",self.mod_name_lastn)
        self.cmbx_Id_Alumno.bind("<KeyRelease>",lambda event:(self.mod_name_lastn(),self.tView.delete(*self.tView.get_children())) )
        
        
        #Label nombres
        self.lblNombres = ttk.Label(self.frm_1, name="lblnombres")
        self.lblNombres.configure(text='Nombre(s):')
        self.lblNombres.place(anchor="nw", x=20, y=130)
        
        #Entry Alumno
        self.nombres = ttk.Entry(self.frm_1, name="nombres",state="readonly")
        self.nombres.place(anchor="nw", width=200, x=110, y=130)
        
        #Label Apellidos
        self.lblApellidos = ttk.Label(self.frm_1, name="lblapellidos")
        self.lblApellidos.configure(text='Apellido(s):')
        self.lblApellidos.place(anchor="nw", x=400, y=130)
        
        #Entry Apellidos
        self.apellidos = ttk.Entry(self.frm_1, name="apellidos",state="readonly")
        self.apellidos.place(anchor="nw", width=200, x=485, y=130)
        
        #Label Curso
        self.lblIdCurso = ttk.Label(self.frm_1, name="lblidcurso")
        self.lblIdCurso.configure(background="#f7f9fd",state="normal",text='Id Curso:')
        self.lblIdCurso.place(anchor="nw", x=20, y=180)
        
        #Entry Curso
        self.id_Curso = ttk.Entry(self.frm_1, name="id_curso")
        self.id_Curso.configure(justify="left", width=166)
        self.id_Curso.place(anchor="nw", width=166, x=100, y=180)
        
        #Label Descripción del Curso
        self.lblDscCurso = ttk.Label(self.frm_1, name="lbldsccurso")
        self.lblDscCurso.configure(background="#f7f9fd",state="normal",text='Curso:')
        self.lblDscCurso.place(anchor="nw", x=275, y=180)
        
        #Entry de Descripción del Curso 
        self.descripc_Curso = ttk.Entry(self.frm_1, name="descripc_curso")
        self.descripc_Curso.configure(justify="left", width=166)
        self.descripc_Curso.place(anchor="nw", width=300, x=325, y=180)
        
        
        ''' Botones  de la Aplicación'''
        #Boton Consultar
        self.btnConsultar=ttk.Button(self.frm_1, name="btnconsultar")
        self.btnConsultar.configure(text="Consultar",command=self.cargar_tV)
        self.btnConsultar.place(anchor="nw", width=100, x=680, y=180)
        
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
        self.btnEliminar.configure(text='Eliminar', )
        self.btnEliminar.place(anchor="nw", x=400, y=220)
        
        #Botón Cancelar
        self.btnCancelar = ttk.Button(self.frm_1, name="btncancelar")
        self.btnCancelar.configure(text='Cancelar', command=self.cancelar_botton)
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
        self.tView_cols = ['tV_descripción','horas','estado']
        self.tView_dcols = ['tV_descripción','horas','estado']
        self.tView.configure(columns=self.tView_cols,displaycolumns=self.tView_dcols)
        self.tView.column("#0",anchor="w",stretch=True,width=10,minwidth=10)
        self.tView.column("tV_descripción",anchor="w",stretch=True,width=200,minwidth=50)
        self.tView.column("horas",anchor="w",stretch=True,width=10,minwidth=10)
        self.tView.column("estado",anchor="w",stretch=True,width=30,minwidth=20)
        
        #Cabeceras
        self.tView.heading("#0", anchor="w", text='ID Curso')
        self.tView.heading("tV_descripción", anchor="w", text='Nombre del Curso')
        self.tView.heading("horas", anchor="w", text='Horas ')
        self.tView.heading("estado", anchor="w", text='Estado de Inscripción')
        self.tView.place(anchor="nw", height=300, width=790, x=4, y=280)
        self.tView.bind("<Button-1>",self.tV_order)
        
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
        
        """La función validacion_size_fecha valida el tamaño de la información
            suministrada en el campo de fecha no sea mayor a 10 caracteres, 
            suprimiendo los caracteres exedentes, ademas de poner automaticamente
            las divisiones de dias, meses y años correspondientes al formato
            de la fecha trabajado"""
        
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
        
        """La función val_fecha valida si la información suministrada en el campo
            de fecha corresponde a una fecha valida o existente"""
        
        if len(self.fecha.get())<=10:
            try:
             # Intentar convertirla a una fecha.
                fechav = datetime.strptime(self.fecha.get(), "%d/%m/%Y")
            except:
                msg.showerror(title="¡Atención!",
                         message="¡Fecha no valida!"
                   )
    
    # Función para ejecutar las instrucciones (query)
    def run_query(self, query):
        
        """La función run_query recibe un query (instruccióna ejecutar sobre la base
            de datos) y retorna una tupla con el resultado de la instrucción."""
        
        with sql.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            conn.commit()
        return cursor.fetchall()

    #Extraer datos de alumnos de la db de forma dinamica
    def update_arrow_IdAlum(self, *args):
        
        """La función update_arrow_IdAlum se encarga de cargar los Id_Alumno
            de la tabla de Alumnos al combobox con su mismo nombre"""
            
        instrc = f"SELECT Id_Alumno FROM Alumnos ORDER BY Id_Alumno"
        self.cmbx_Id_Alumno['values']=self.run_query(instrc)
        self.serch_Id_Alum()
            
    #Cuando se escriba en el combobox de Id Alumnos buscar coincidencias
    def serch_Id_Alum(self):
        
        """La función serch_Id_Alum busca coincidencias en la tablan de Alumnos
            con el Id_Alumno escrito por el usuario para reducir la cantidad
            de registros mostrados en el combobox. En caso de no encontrar una
            coincidencia mostrara un letrero de advertencia."""
            
        self.tView.delete(*self.tView.get_children())
        instrc = f"SELECT Id_Alumno FROM Alumnos WHERE Id_Alumno like '%{self.idAlumSelect.get()}%'"
        resultados=self.run_query(instrc)
        
        # Para saber si la busqueda no retorno nada
        if resultados:
   
            if (self.idAlumSelect.get()!=resultados[0][0] or len(resultados)!=1) and len(resultados)!=0:
            
                self.cmbx_Id_Alumno['values']=resultados
                
        else:

            msg.showerror(title="¡Atención!",
                         message="¡Id de Alumno no valido!"
                   )
            self.cmbx_Id_Alumno.delete(0,tk.END)
    
    #Cuando se seleccione el codigo, se llene los campos de nombres y apellidos
    def info_Alum(self,event):
        
        """La función info_Alum muestra en los campos de nombres y apellidos 
            los datos correspondientes a el id seleccionado en el combobox
            de Id_Alumnos"""
    
        datos = self.run_query(f"SELECT Nombres, Apellidos FROM Alumnos WHERE Id_Alumno='{self.idAlumSelect.get()}' ORDER BY Id_Alumno")
       
        #Insertar en los entrys nombres y apellidos
        self.mod_name_lastn(datos[0][0],datos[0][1])
       
    
    def cancelar_botton(self):
        
        """La función cancelar_botton limpia todos los campos de la venta para
            poder ingresar nueva información"""
        # limpiar el tree view
        self.tView.delete(*self.tView.get_children())
            
        # limpiar el campo de No.Inscripción
        self.num_Inscripcion.delete(0,tk.END)

        #limpiar el campo de fecha
        self.fecha.delete(0,tk.END)
        self.fecha.insert(0, "dd/mm/aaaa")
        
        # limpiar el campo de cmbx_Id_Alumno
        self.cmbx_Id_Alumno.delete(0,tk.END)

        # limpiar los campos de nombres y apellidos
        self.mod_name_lastn()

        # limpiar los campos de Id Curso, Curso y Hora
        self.id_Curso.delete(0,tk.END)
        self.descripc_Curso.delete(0,tk.END)
        self.horario.delete(0,tk.END)

        
    
    def mod_name_lastn(self,nombre=None,apellido=None,*args):
        
        # limpiar los campos de nombres y apellidos
        self.nombres.config(state="normal")
        self.apellidos.config(state="normal")

        self.nombres.delete(0,tk.END)
        self.apellidos.delete(0,tk.END)

        
        # si se pasan argumentos, ponerlos en los entrys respectivos
        if nombre and apellido:
            self.nombres.insert(0,nombre)
            self.apellidos.insert(0,apellido)
        
        self.nombres.config(state="readonly")
        self.apellidos.config(state="readonly")
    
    def cargar_tV(self, orden="Código_Curso"):
    

    # Obteniendo los valores ingresados por el usuario
     filtro_id_curso = self.id_Curso.get().strip()
     filtro_descripcion_curso = self.descripc_Curso.get().strip()

    # Construyendo la consulta SQL con los filtros necesarios
     query = "SELECT * FROM Cursos"
     conditions = []
    
     if filtro_id_curso:
        conditions.append(f"Código_Curso LIKE '%{filtro_id_curso}%'")
     if filtro_descripcion_curso:
        conditions.append(f"Descripción LIKE '%{filtro_descripcion_curso}%'")
    
     if conditions:
        query += " WHERE " + " AND ".join(conditions)
    
     query += f" ORDER BY {orden}"

    # Ejecutando la consulta y actualizando el TreeView
     cursos = self.run_query(query)
     self.tView.delete(*self.tView.get_children())
     for curso in cursos:
        estado = "No Inscrito"
        datos = self.run_query(f"SELECT Código_Curso FROM Inscritos WHERE Id_Alumno='{self.idAlumSelect.get()}'")
        if datos and curso[0] in [d[0] for d in datos]:
            estado = "Inscrito"
        self.tView.insert("", "end", text=curso[0], values=(curso[1], curso[2], estado))



    def tV_order(self,event):
        
        """La función tv_order identifica en que heading se ha seleccionado
            para poder organizar los datos por medio de ese parametro"""
            
        colum_id = self.tView.identify_column(event.x)
        if colum_id=="#0":
            self.cargar_tV()
        elif colum_id=="#1":
            self.cargar_tV("Descripción")
        elif colum_id=="#2":
            self.cargar_tV("Num_Horas")
            
    
if __name__ == "__main__":
    app = Inscripciones()
    app.run()
