# !/usr/bin/python3
# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import messagebox as msg
import tkinter.ttk as ttk
import sqlite3 as sql
from datetime import datetime
from datetime import date
from os import path

class Inscripciones:
    
    def __init__(self, master=None):
        # Ventan principal 
        self.ruta_proyecto = __file__.replace(path.basename(__file__), "")
        self.ruta_imagen = path.abspath(self.ruta_proyecto + "img/icono2.png")
        ruta_db = path.abspath(self.ruta_proyecto + "db/Inscripciones.db")

        self.db_name =  ruta_db #establecer la ruta de la db
        self.win = tk.Tk(master)
        self.win.configure(background="#f7f9fd") #fondo ventana
        geometry=self.centrar_ventana(800,600,self.win)
        self.win.geometry(f"{geometry}")
        
        self.win.resizable(False, False)
        self.win.title("Inscripciones de Materias y Cursos")
        self.win.iconphoto(False, tk.PhotoImage(file=self.ruta_imagen))
        
        # Crea los frames
        self.frm_1 = tk.Frame(self.win, name="frm_1")
        self.frm_1.configure(background="#f7f9fd", height=600, width=800)
        self.lblNoInscripcion = ttk.Label(self.frm_1, name="lblnoinscripcion")
        self.lblNoInscripcion.configure(background="#f7f9fd",font="{Arial} 11 {bold}",
                                        justify="left",state="normal",
                                        takefocus=False,text='No.Inscripción')
        
        #Label No. Inscripción
        self.lblNoInscripcion.place(anchor="nw", x=680, y=20)
        
        #Combobox No. Inscripción
        self.no_Inscrip_Select = tk.StringVar()
        self.num_Inscripcion = ttk.Combobox(self.frm_1, name="num_inscripcion", state="readonly", 
                                           postcommand=self.cargar_No_Inscripciones, 
                                           textvariable=self.no_Inscrip_Select)
        self.num_Inscripcion.configure(justify="right")
        self.num_Inscripcion.place(anchor="nw", width=100, x=682, y=42)
        self.num_Inscripcion.bind("<<ComboboxSelected>>", self.info_Alum_For_Inscrp) #Rellenar los campos segun el No. Inscripción
        
        
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
        self.id_Alum_Select=tk.StringVar()
        self.cmbx_Id_Alumno = ttk.Combobox(self.frm_1,
                                           name="cmbx_id_alumno", 
                                           postcommand=self.update_arrow_IdAlum , 
                                           textvariable=self.id_Alum_Select)
        self.cmbx_Id_Alumno.place(anchor="nw", width=112, x=110, y=85)
        # Actualizar la info cuando se selecciona una opción de la lista desplegable
        self.cmbx_Id_Alumno.bind("<<ComboboxSelected>>", lambda event: (self.info_Alum(),self.asignacion_No_Inscripcion())) #Rellenar el No. Inscripción segun el Alumno
        #cada que se oprima alguna tecla en el campo de id Alumno, limpiar los campos que se llenan automaticamente
        self.cmbx_Id_Alumno.bind("<KeyRelease>",lambda event:(self.mod_name_lastn(),self.tView.delete(*self.tView.get_children()),self.id_Curso.delete(0,tk.END),self.descripc_Curso.delete(0,tk.END), self.num_Inscripcion.set("")))
        
        
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
        # al presionar el boton, se debe confirmar que se halla ingresado un alumno para desplegar los cursos
        self.btnConsultar.configure(text="Consultar",command=lambda: self.opciones("S"))
        self.btnConsultar.place(anchor="nw",width=100, x=670, y=180)

        #Botón Guardar
        self.btnGuardar = ttk.Button(self.frm_1, name="btnguardar")
        self.btnGuardar.configure(text='Guardar',command=lambda: self.opciones("G"))
        self.btnGuardar.place(anchor="nw", x=200, y=240)
        
        #Botón Editar
        self.btnEditar = ttk.Button(self.frm_1, name="btneditar")
        self.btnEditar.configure(text='Editar',command=lambda: self.opciones("E"))
        self.btnEditar.place(anchor="nw", x=300, y=240)
        
        #Botón Eliminar
        self.btnEliminar = ttk.Button(self.frm_1, name="btneliminar")
        self.btnEliminar.configure(text='Eliminar',command=lambda: self.opciones("D"))
        self.btnEliminar.place(anchor="nw", x=400, y=240)
        
        #Botón Cancelar
        self.btnCancelar = ttk.Button(self.frm_1, name="btncancelar")
        self.btnCancelar.configure(text='Cancelar',command=lambda: self.opciones("C"))
        self.btnCancelar.place(anchor="nw", x=500, y=240)
        
        #Botón Fecha de hoy
        self.btnFechaHoy = ttk.Button(self.frm_1, name="btnfechahoy")
        self.btnFechaHoy.configure(text='+', padding=(0,-5),command=self.fecha_Hoy)
        self.btnFechaHoy.place(anchor="nw",width=20, height=20,x=775, y=81)
        
        
        #Separadores
        separator1 = ttk.Separator(self.frm_1)
        separator1.configure(orient="horizontal")
        separator1.place(anchor="nw", width=796, x=2, y=225)


        ''' Treeview de la Aplicación'''
        
        #Treeview
        self.tView = ttk.Treeview(self.frm_1, name="tview")
        self.tView.configure(selectmode="extended")
        
        
        #Columnas del Treeview
        self.tView_cols = ['tV_descripción','horas','estado','Jornada']
        self.tView_dcols = ['tV_descripción','horas','estado','Jornada']
        self.tView.configure(columns=self.tView_cols,displaycolumns=self.tView_dcols)
        self.tView.column("#0",anchor="w",stretch=True,width=20,minwidth=10)
        self.tView.column("tV_descripción",anchor="w",stretch=True,width=200,minwidth=50)
        self.tView.column("horas",anchor="w",stretch=True,width=5,minwidth=10)
        self.tView.column("estado",anchor="w",stretch=True,width=30,minwidth=20)
        self.tView.column("Jornada",anchor="w",stretch=True,width=20,minwidth=20)
        
        #Cabeceras
        self.tView.heading("#0", anchor="w", text='ID Curso')
        self.tView.heading("tV_descripción", anchor="w", text='Nombre del Curso')
        self.tView.heading("horas", anchor="w", text='Horas ')
        self.tView.heading("estado", anchor="w", text='Estado de Inscripción')
        self.tView.heading("Jornada", anchor="w", text='Jornada')
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
            
        #Borrar todos los espacios de la fecha
        fecha=self.fecha.get()
        if " " in fecha:
            self.fecha.delete(0,tk.END)
            self.fecha.insert(0,fecha.replace(" ",""))
        
        #insertar "/"" automatico para separar dias, mese y años
        if len(self.fecha.get())==2 or len(self.fecha.get())==5:
            self.fecha.insert(tk.END,"/")
            
        #Verificación de maximo de caracteres permitidos en fecha
        elif len(self.fecha.get())>10:
            msg.showerror(title="¡Atención!",message="-Maximo 10 caracteres-")
            self.fecha.delete(10, tk.END) #borrar caracteres demas
            
    #Verificar si la fecha digitada es valida
    def val_fecha(self):
        
        """La función val_fecha valida si la información suministrada en el campo
            de fecha corresponde a una fecha valida o existente"""
        
        if len(self.fecha.get())<=10:
            
            if self.verificacion_fecha():
                pass
            else:
                msg.showerror(title="¡Atención!",message="¡Fecha no valida!")
    
    #Función verificacion fecha
    def verificacion_fecha(self):
        
        """La función verificacion de fecha valida si la fecha es correcta o no
            retornando True o False"""
            
        fecha=True
        try:
        # Intentar convertirla a una fecha.
            fechav = datetime.strptime(self.fecha.get(), "%d/%m/%Y")
        except:
            fecha=False
        return fecha
    
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
    def update_arrow_IdAlum(self, *event):
        
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
        
        instrc = f"SELECT Id_Alumno FROM Alumnos WHERE Id_Alumno LIKE '%{self.id_Alum_Select.get()}%'"
        resultados=self.run_query(instrc)
        
        # Para saber si la busqueda no retorno nada
        if resultados:
   
            if (self.id_Alum_Select.get()!=resultados[0][0] or len(resultados)!=1) and len(resultados)!=0:
            
                self.cmbx_Id_Alumno['values']=resultados
                
        else:

            msg.showerror(title="¡Atención!",message="¡Id de Alumno no valido!")
            self.cmbx_Id_Alumno.delete(0,tk.END)
    
    #Cuando se seleccione el codigo, se llene los campos de nombres y apellidos
    def info_Alum(self,*event):
        
        """La función info_Alum muestra en los campos de nombres y apellidos 
            los datos correspondientes a el id seleccionado en el combobox
            de Id_Alumnos"""
    
        datos = self.run_query(f"SELECT Nombres, Apellidos FROM Alumnos WHERE Id_Alumno='{self.id_Alum_Select.get()}' ORDER BY Id_Alumno")
       
        #Insertar en los entrys nombres y apellidos
        self.mod_name_lastn(datos[0][0],datos[0][1])
        self.id_Curso.delete(0,tk.END)
        self.descripc_Curso.delete(0,tk.END)
        self.cargar_tV()
    
    #Modificar nombres y apellidos
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
    
    #Cargar datos en el treeView
    def cargar_tV(self,orden="Código_Curso",inscrito=False):
        
        """La función cargar_tV sirve para cargar en el treeView los datos de los 
            cursos encontrados en la base de datos"""

        self.tView.delete(*self.tView.get_children())
        estado="No Inscrito"
        
        #Organizar por estado de inscripción
        if inscrito:
            
            # Buscar las coincidencias entre la tabla de cursos y la de inscritos con base a un alumno
            query =f""" SELECT Cursos.*, Inscritos.Jornada FROM Cursos INNER JOIN Inscritos 
                    ON Inscritos.Código_Curso = Cursos.Código_Curso 
                    WHERE No_Inscripción = '{self.num_Inscripcion.get()}' ORDER BY {orden}"""
            
            cursos=self.run_query(query)
            
            if len(cursos)!=0:
                estado="Inscrito"
                for curso in cursos:
                    jornada=curso[-1]
                    self.tView.insert("","end",text=curso[0],values=(curso[1],curso[2],estado,jornada))
            
            estado="No Inscrito"
            jornada="..."
            
            # Busca todos los cursos qeu no aparezcan en la tabla de inscritos para el alumno seleccionado
            query =f"""SELECT Cursos.* FROM Cursos LEFT JOIN Inscritos 
                    ON Cursos.Código_Curso = Inscritos.Código_Curso and Inscritos.No_Inscripción = '{self.num_Inscripcion.get()}' 
                    WHERE Inscritos.Código_Curso IS NULL ORDER BY {orden}"""
            
            cursos=self.run_query(query)

            for curso in cursos:
                    self.tView.insert("","end",text=curso[0],values=(curso[1],curso[2],estado,jornada))
            
        else:
            query="SELECT * FROM Cursos"
            
            if self.id_Curso.get()!="":
                query +=f" WHERE Código_Curso LIKE '%{self.id_Curso.get()}%' "
            elif self.descripc_Curso.get()!="":
                query +=f" WHERE Descripción LIKE '%{self.descripc_Curso.get()}%' "   
                
            query += f" ORDER BY {orden}"
            cursos=self.run_query(query)
            
            #ingresar cada registro en el tV
            for curso in cursos:
                estado="No Inscrito"
                jornada="..."   
                datos=self.run_query(f"SELECT Código_Curso FROM Inscritos WHERE Id_Alumno='{self.id_Alum_Select.get()}'")

                #  Para saber el estado del curso con respecto al estudiante, se debe de conocer 
                #  si el curso ya se encuentra en la tabla de inscritos asociado a el Id del alumno
                if len(datos)!=0:
                    for dato in datos: 
                        if curso[0] == dato[0]: 
                            estado="Inscrito"
                            jornada=self.run_query(f"SELECT Jornada FROM Inscritos WHERE Código_Curso='{curso[0]}' and Id_Alumno='{self.id_Alum_Select.get()}'")[0][0]
                        
                #agregar info al treeview
                self.tView.insert("","end",text=curso[0],values=(curso[1],curso[2],estado,jornada))
    
    #Determina que cabecera se ha seleccionado para organizarlo
    def tV_order(self,event):
        
        """La función tv_order identifica que heading se ha seleccionado
            para poder organizar los datos por medio de ese parametro"""
            
        if self.apellidos.get()!="" or self.nombres.get()!="":
            
            colum_id = self.tView.identify_column(event.x)
            position_y = self.tView.identify_region(y=event.y,x=event.x)

            if colum_id=="#0" and position_y=="heading":
                self.cargar_tV()
            elif colum_id=="#1" and position_y=="heading":
                self.cargar_tV("Descripción")
            elif colum_id=="#2" and position_y=="heading":
                self.cargar_tV("Num_Horas")
            elif colum_id=="#3" and position_y=="heading":
                self.cargar_tV(inscrito=True)

    #Asigna un numero de inscripcion al alumno
    def asignacion_No_Inscripcion(self):
        
        """La función asignacion_No_Inscripcion sirve para generar el No_Inscripción.
            Para generar el No_Inscripción se debe de tener en cuenta que el No_Inscripción
            debe de ser unico para cada estudiante, buscando en la base de datos si ya hay
            un No_Inscripción creado para ese estudiante, y si no, se le asigna el siguiente
            al ultimo No_Inscripción creado"""
        
        query = f"SELECT DISTINCT No_Inscripción FROM Inscritos WHERE Id_Alumno = {self.id_Alum_Select.get()} ORDER BY No_Inscripción DESC"
        inscripciones=self.run_query(query)
        
        if len(inscripciones) == 0:
            no_Exis=self.run_query("SELECT Valor FROM Variables_Numericas WHERE Nombre = 'No_Inscripciones'")
            self.num_Inscripcion.set(no_Exis[0][0]+1)
            
        else:
            self.num_Inscripcion.set(inscripciones[0][0])
    
    #Alimenta el combobox de No. de inscripciones
    def cargar_No_Inscripciones(self):
        
        """La función cargar_No_Inscripciones sirve para cargar en el tcmx los No_Inscripciones
            encontrados en la base de datos"""
        
        query = "SELECT DISTINCT No_Inscripción FROM Inscritos ORDER BY No_Inscripción DESC"
        inscritos=self.run_query(query)
        self.num_Inscripcion['values']=inscritos
    
    #Carga la info del alumno segun el No. de inscripción
    def info_Alum_For_Inscrp(self,event):
        
        """La función info_Alum_For_Inscrp identifica el No. de inscripción seleccionado
            para mostrar la informacion de ese estudiante"""

        query=f"SELECT DISTINCT Id_Alumno FROM Inscritos WHERE No_Inscripción='{self.num_Inscripcion.get()}'"
        datos=self.run_query(query)
        self.id_Alum_Select.set(datos[0][0])
        self.info_Alum(event)
    
    #Metodo para centrar la ventana
    def centrar_ventana(self,wwin,hwin,win):
        
        """La función centrar_ventana centra la ventana en la pantalla del usuario"""
        
        px = round(win.winfo_screenwidth()/2-wwin/2)
        py = round(win.winfo_screenheight()/2-hwin/2)
        return str(wwin)+"x"+str(hwin)+"+"+str(px)+"+"+str(py)

    #Metodo para cargar la fecha de hoy
    def fecha_Hoy(self):
        
        fecha=f"{date.today().day}/{date.today().month}/{date.today().year}"
        self.fecha.delete(0,tk.END)
        if date.today().day<10 and date.today().month<10:
            fecha=f"0{date.today().day}/0{date.today().month}/{date.today().year}"
        elif date.today().month<10:
            fecha=f"{date.today().day}/0{date.today().month}/{date.today().year}"
        else:
            fecha=f"0{date.today().day}/{date.today().month}/{date.today().year}"
        self.fecha.insert(0,fecha)
    
    #ventana emergente para la selccion de jornada
    def eleccion_jornada(self,id_Curso,curso):
        
        """La función eleccion_jornada se encarga de generar una ventana
            emergente para la elección de la jornada del curso a inscribir"""
        
        #variable para dejar continuar la función si se oprime algun boton
        interruptor=tk.BooleanVar(value=False)
        
        resultado=tk.StringVar()
        winEmergente= tk.Toplevel()
        winEmergente.resizable(0,0)
        geometry=self.centrar_ventana(300,160,winEmergente)
        winEmergente.geometry(f"{geometry}")
        winEmergente.title("Inscripcción de curso")
        winEmergente.iconphoto(False, tk.PhotoImage(file=self.ruta_imagen))
        
        #para evitar que se pueda usar otra ventana mientras winEmergente este abierto
        winEmergente.grab_set()
        winEmergente.focus_set()

        #para cuando se cierra la ventana emergente se activa el interruptor
        winEmergente.protocol("WM_DELETE_WINDOW", lambda: (interruptor.set(True),
                                                           resultado.set("")))
        
        frm = tk.Frame(winEmergente, name="frm_1")
        frm.configure(background="#f7f9fd", height=160, width=300)
        
        lblInfo=ttk.Label(frm, name="lblinfo")
        lblInfo.configure(background="#f7f9fd",state="normal",
                          text="Ha seleccionado el siguiente curso para inscribir:"
                          )
        lblInfo.place(anchor="center", x=150, y=15)
        
        
        lblCurso= ttk.Label(frm, name="lblcurso")
        lblCurso.configure(background="#90EE90",state="normal",text=f"ID: {id_Curso}  | Curso: {curso}")
        lblCurso.place(anchor="center", x=150, y=45)
        
        lblJornada = ttk.Label(frm, name="lbljornada")
        lblJornada.configure(background="#f7f9fd",state="normal",
                          text=f"Seleccione la jornada en la que desea ver el curso:"
                          )
        lblJornada.place(anchor="center", x=150, y=75)
        
        jornada=tk.StringVar()
        cmbx_Jornada = ttk.Combobox(frm, name="cmbx_jornada",state="readonly",values=["Diurna","Nocturna","Mixta"],textvariable=jornada)
        cmbx_Jornada.place(anchor="center", x=150, y=105)
        
        btnConfirmar=ttk.Button(frm, name="btnconfirmar")
        btnConfirmar.configure(text="Confirmar",command=lambda: (interruptor.set(True),resultado.set(jornada.get()))
                                                                if jornada.get() != "" 
                                                                else  msg.showerror("Error", "Por favor seleccione la jornada"))
        btnConfirmar.place(anchor="nw",width=90 , x=50, y=130)
        
        btnCancelar=ttk.Button(frm, name="btncancelar")
        btnCancelar.configure(text="Cancelar", command=lambda: (interruptor.set(True),resultado.set("")))
        btnCancelar.place(anchor="nw",width=90 , x=160, y=130)
        frm.pack()
        
        #Espera a que el interruptor se active para qeu continue la ejecucion
        winEmergente.wait_variable(interruptor)
        
        winEmergente.destroy()
        return resultado.get()
        
    #==============================================================================
    # Funcionalidad de los botones
    
    def guardar_botton(self):
        
        # obtener la fila seleccionada del tree view
        current_item_id = self.tView.focus()
        current_item = self.tView.item(current_item_id)
        if current_item["text"] == "":
            msg.showerror("Error", "Por favor seleccione una fila")
            return
        if current_item["values"][2].lower() == "inscrito":
            msg.showerror("Error", "El estudiante ya esta inscrito en el curso")
            return

        id_alumno = self.cmbx_Id_Alumno.get()
        fecha_inscripcion = self.fecha.get()
        codigo_curso = current_item["text"]
        no_Inscripcion = self.num_Inscripcion.get()
        
        #verifica si la fecha a ingresar en la db es valida
        if self.verificacion_fecha():

            jornada = self.eleccion_jornada(codigo_curso,current_item["values"][0])
            
            if jornada:
                
                 # añadir la inscripcion a la base de datos
                self.run_query(f"INSERT INTO Inscritos (No_Inscripción,Id_Alumno,Fecha_Inscripción,Código_Curso,Jornada) VALUES ('{no_Inscripcion}','{id_alumno}','{fecha_inscripcion}','{codigo_curso}','{jornada}')")

                # actualizar el estado de inscripción (visualmente)
                current_item["values"][2] = "Inscrito"
                current_item["values"][3] = jornada
                self.tView.item(item=current_item_id, values=current_item["values"])
                max_no=self.run_query("SELECT MAX(No_Inscripción) FROM Inscritos")
                #print(max_no,type(max_no),max_no[0][0],type(max_no[0][0]),no_Inscripcion,type(no_Inscripcion))
                
                # Saber si es la ultima inscripción
                if max_no[0][0]==int(no_Inscripcion):
                    #hasta no inscribir la materia, no generar nuevo no de inscripción
                    self.run_query(f"UPDATE Variables_Numericas SET Valor = {no_Inscripcion} WHERE Nombre = 'No_Inscripciones'")
                
                msg.showinfo("Info", "Alumno inscrito exitosamente")
        
        else: 

            msg.showerror(title="¡Atención!",message="¡Fecha no valida!")

    def cancelar_botton(self):
        
        """La función cancelar_botton limpia todos los campos de la venta para
            poder ingresar nueva información"""
            

        #limpiar el campo de fecha
        self.fecha.delete(0,tk.END)
        self.fecha.insert(0, "dd/mm/aaaa")
        
        # limpiar el campo de cmbx_Id_Alumno y num_Inscripcion
        self.cmbx_Id_Alumno.delete(0,tk.END)
        self.no_Inscrip_Select.set("")

        # limpiar los campos de nombres y apellidos
        self.mod_name_lastn()

        # limpiar los campos de Id Curso, Curso y Hora
        self.id_Curso.delete(0,tk.END)
        self.descripc_Curso.delete(0,tk.END)

        # limpiar el tree view
        self.tView.delete(*self.tView.get_children())
    
    def delete_botton(self):
        
        """La función delete_botton elimina la inscripción seleccionada en el tree view.
            Si no se selecciona ningun campo del tree view, se eliminnara todas las inscripciones
            de ese No. de inscripción"""
        
        current_item_id = self.tView.focus()
        current_item = self.tView.item(current_item_id)
        
        if current_item["text"] == "":
            
            query=f"SELECT * FROM Inscritos WHERE No_Inscripción='{self.num_Inscripcion.get()}'"
            existencia=self.run_query(query)
            
            if len(existencia)==0:
                msg.showerror("Error", "¡No hay inscripciones para eliminar!")
            else:
                texto=(self.id_Alum_Select.get()+" - "+self.nombres.get()+" "+self.apellidos.get()).center(60)
                texto1="Esta por eliminar todos los cursos inscritos por:".center(60)
                if msg.askokcancel("Eliminar", f"""{texto1}\n\n{texto}"""):
                    
                    query = f"DELETE FROM Inscritos WHERE No_Inscripción='{self.num_Inscripcion.get()}'"
                    self.run_query(query)
                    msg.showinfo("Eliminar", "Eliminación exitosa")
                    self.cargar_tV(inscrito=True)
                
        elif current_item["values"][2].lower() == "inscrito":
            texto1="Esta por eliminar el curso inscrito:".center(60)
            texto=("ID: "+current_item["text"]+" | Curso: "+current_item["values"][0]).center(60)
            if msg.askokcancel("Eliminar", f"""{texto1}\n\n{texto}"""):
                
                query = f"DELETE FROM Inscritos WHERE No_Inscripción='{self.num_Inscripcion.get()}' and Código_Curso='{current_item['text']}'"
                self.run_query(query)
                msg.showinfo("Eliminar", "Eliminación exitosa")
                self.cargar_tV(inscrito=True)
        else:
            msg.showerror("Error", "El estudiante no esta inscrito en el curso")
    
    def editar_botton(self):
        
        # obtener la fila seleccionada del tree view
        current_item_id = self.tView.focus()
        print(current_item_id)
        current_item = self.tView.item(current_item_id)
        if current_item["text"] == "":
            msg.showerror("Error", "Por favor seleccione una fila")
            return
        if current_item["values"][2].lower() == "no inscrito":
            msg.showerror("Error", "El estudiante no esta inscrito en el curso")
            return
        
        fecha_inscripcion = self.fecha.get()
        codigo_curso = current_item["text"]
        #no_Inscripcion = self.num_Inscripcion.get()
        jornada=current_item["values"][-1]
        descripc_curso = current_item["values"][0]
        no_Inscripcion = self.num_Inscripcion.get()
        
        if self.verificacion_fecha():
            
            #almacernar modificaciones
            mod=self.ventana_edicion(codigo_curso,descripc_curso,no_Inscripcion,jornada)
            
            if len(mod)==1:
                self. run_query(f"""UPDATE Inscritos SET Fecha_Inscripción = '{fecha_inscripcion}', Jornada = '{mod[0]}' 
                                WHERE Código_Curso = '{codigo_curso}' and No_Inscripción = '{no_Inscripcion}'""")
                
                current_item["values"][3] = mod[0]
                self.tView.item(item=current_item_id, values=current_item["values"])
                
            elif len(mod)==2:
                self.run_query(f"""UPDATE Inscritos SET Código_Curso = '{mod[0]}', Fecha_Inscripción = '{fecha_inscripcion}', Jornada = '{mod[1]}'
                               WHERE Código_Curso = '{codigo_curso}' and No_Inscripción = '{no_Inscripcion}'"""
                )
                current_item["values"][-1] = "..."
                current_item["values"][-2] = "No Inscrito"
                self.tView.item(item=current_item_id, values=current_item["values"])
                
                #Para cambiar el estado de inscripción y jornada del treeview
                for item in self.tView.get_children():
                    
                    #identificar que fila es la del curso modificado
                    if self.tView.item(item)["text"] == mod[0]:
                        
                        #cambiar el estado de inscripción y jornada
                        current_item = self.tView.item(item)
                        current_item["values"][-2] = "Inscrito"
                        current_item["values"][-1] = mod[1]
                        self.tView.item(item=item, values=current_item["values"])

        msg.showinfo("Info", "Curso editado exitosamente")
    
    
    #La manera correcta de hacer las ventanas emergentes son creando una nueva clase, pero por el momento lo dejamos asi
    #ya que, en los requerimientos no dice nada :b (en futuro se puede arreglar pero implica hacer más funciones e
    # implementar callbacks en la nueva clase)
    
    def ventana_edicion(self,id_Curso_Seleccionado,curso_Seleccionado,no_Inscripcion_Seleccionado,jornada_Seleccionada):
        
        """La función ventana_edicion se encarga de crear una nueva ventana emergente
            para poder editar la inscripción seleccionada. Se le da la posibilidad de
            modificar la jornada del curso o el mismo curso"""
        
        #variable para dejar continuar la función si se oprime algun boton
        interruptor=tk.BooleanVar(value=False)
        
        resultado=tk.StringVar()
        winEmergente= tk.Toplevel()
        winEmergente.resizable(0,0)
        geometry=self.centrar_ventana(620,200,winEmergente)
        winEmergente.geometry(f"{geometry}")
        winEmergente.title("Edición de inscripción")
        winEmergente.iconphoto(False, tk.PhotoImage(file=self.ruta_imagen))
        
        #==========================================================================
        #Frame para el cambio de jornada de un curso
        
        frm = tk.Frame(winEmergente, name="frm")
        frm.configure(background="#f7f9fd", height=75, width=620)
        
        #para evitar que no se pueda usar otra ventana mientras winEmergente este abierto
        winEmergente.grab_set()
        winEmergente.focus_set()
        
        lblCambioJornada = ttk.Label(frm, name="lblcambiorjornada")
        lblCambioJornada.configure(background="#f7f9fd",state="normal",text='Cambio de jornada del curso seleccionado:')
        lblCambioJornada.place(anchor="w", x=20, y=20)
        
        
        lblIdCurso = ttk.Label(frm, name="lblidcurso")
        lblIdCurso.configure(background="#f7f9fd",state="normal",text='Id Curso:')
        lblIdCurso.place(anchor="w", x=20, y=50)
        
        id_Curso = ttk.Entry(frm, name="id_curso")
        id_Curso.configure(justify="left", width=166)
        id_Curso.insert(0,id_Curso_Seleccionado)
        id_Curso.configure(state="readonly")
        id_Curso.place(anchor="w", width=90, x=80, y=50)
        
        lblDscCurso = ttk.Label(frm, name="lbldsccurso")
        lblDscCurso.configure(background="#f7f9fd",state="normal",text='Curso:')
        lblDscCurso.place(anchor="w", x=190, y=50)
        
        descripc_Curso = ttk.Entry(frm, name="descripc_curso")
        descripc_Curso.configure(justify="left", width=166)
        descripc_Curso.insert(0,curso_Seleccionado)
        descripc_Curso.configure(state="readonly")
        descripc_Curso.place(anchor="w", width=200, x=240, y=50)
        
        lblJornada = ttk.Label(frm, name="lbljornada")
        lblJornada.configure(background="#f7f9fd",state="normal",text='Jornada:')
        lblJornada.place(anchor="w", x=460, y=50)
        
        jornadas=["Diurna","Nocturna","Mixta"]
        jornadas.remove(jornada_Seleccionada)
        
        new_Jornada=tk.StringVar()
        cmbx_Jornada = ttk.Combobox(frm, name="cmbx_jornada",state="readonly",
                                    values=jornadas,textvariable=new_Jornada)
        cmbx_Jornada.place(anchor="w",width=80, x=515, y=50)
        
        separator1 = ttk.Separator(frm)
        separator1.configure(orient="horizontal")
        separator1.place(anchor="sw", width=612, x=4, y=74)
        
        
        #============================================================================
        #Frame para cambio de curso
        
        frm_2 = tk.Frame(winEmergente, name="frm_2")
        frm_2.configure(background="#A9A9A9", height=75, width=620)
        
        cursos=self.run_query(f"""SELECT Cursos.Código_Curso, Cursos.Descripción 
                              FROM Cursos LEFT JOIN Inscritos
                              ON Cursos.Código_Curso = Inscritos.Código_Curso and Inscritos.No_Inscripción = '{no_Inscripcion_Seleccionado}'
                              WHERE Inscritos.Código_Curso IS NULL ORDER BY Cursos.Código_Curso""")
        
        id_Cursos=[curso[0] for curso in cursos]
        descrip_Cursos=[curso[1] for curso in cursos]
            
        #Checkbox para confirmar la edición (esta en un lamda porque hacer un afuncion dentro de una
        # fución esta un poco xd)
        
        checkbox_value = tk.BooleanVar()
        checkbox = ttk.Checkbutton(frm_2, name="checkbox",text="Cambiar de curso inscrito.",
                                   variable=checkbox_value,
                                   command=lambda: (cmbx_Descrip_Curso.configure(state="readonly"),
                                                    cmbx_Jornada.configure(state="disabled"),
                                                    cmbx_Jornada_New.configure(state="readonly"),
                                                    cmbx_Id_Curso.configure(state="readonly"),
                                                    frm_2.configure(background="#f7f9fd"),
                                                    lblCambioJornada.configure(background="#A9A9A9"),
                                                    lblDscCurso.configure(background="#A9A9A9"),
                                                    lblIdCurso.configure(background="#A9A9A9"),
                                                    lblDscCursoNew.configure(background="#f7f9fd"),
                                                    lblIdCursoNew.configure(background="#f7f9fd"),
                                                    lblJornadaNew.configure(background="#f7f9fd"),
                                                    frm.configure(background="#A9A9A9")
                                                    )if checkbox_value.get() else 
                                                    (cmbx_Descrip_Curso.configure(state="disabled"),
                                                    cmbx_Jornada.configure(state="readonly"),
                                                    cmbx_Jornada_New.configure(state="disabled"),
                                                    cmbx_Id_Curso.configure(state="disabled"),
                                                    frm_2.configure(background="#A9A9A9"),
                                                    lblCambioJornada.configure(background="#f7f9fd"),
                                                    lblDscCurso.configure(background="#f7f9fd"),
                                                    lblIdCurso.configure(background="#f7f9fd"),
                                                    lblDscCursoNew.configure(background="#A9A9A9"),
                                                    lblIdCursoNew.configure(background="#A9A9A9"),
                                                    lblJornadaNew.configure(background="#A9A9A9"),
                                                    frm.configure(background="#f7f9fd")
                                                    ))
        checkbox.place(anchor="w", x=20, y=20)
        
        lblIdCursoNew = ttk.Label(frm_2, name="lblidcurso")
        lblIdCursoNew.configure(background="#A9A9A9",state="normal",text='Id Curso:')
        lblIdCursoNew.place(anchor="w", x=20, y=50)
        
        id_Curso_Select = tk.StringVar()
        cmbx_Id_Curso = ttk.Combobox(frm_2, name="id_curso")
        cmbx_Id_Curso.configure(justify="left", width=166,values=id_Cursos,state="disabled",textvariable=id_Curso_Select)
        cmbx_Id_Curso.place(anchor="w", width=90, x=80, y=50)
        cmbx_Id_Curso.bind("<<ComboboxSelected>>", lambda event: (descripc_Curso_Select.set(descrip_Cursos[id_Cursos.index(cmbx_Id_Curso.get())])))
        
        lblDscCursoNew = ttk.Label(frm_2, name="lbldsccurso")
        lblDscCursoNew.configure(background="#A9A9A9",state="normal",text='Curso:')
        lblDscCursoNew.place(anchor="w", x=190, y=50)
        
        descripc_Curso_Select = tk.StringVar()
        cmbx_Descrip_Curso = ttk.Combobox(frm_2, name="descripc_curso")
        cmbx_Descrip_Curso.configure(justify="left", width=166,values=descrip_Cursos,state="disabled",textvariable=descripc_Curso_Select)
        cmbx_Descrip_Curso.place(anchor="w", width=200, x=240, y=50)
        cmbx_Descrip_Curso.bind("<<ComboboxSelected>>", lambda event: (id_Curso_Select.set(id_Cursos[descrip_Cursos.index(cmbx_Descrip_Curso.get())])))
        
        lblJornadaNew = ttk.Label(frm_2, name="lbljornada")
        lblJornadaNew.configure(background="#A9A9A9",state="normal",text='Jornada:')
        lblJornadaNew.place(anchor="w", x=460, y=50)
        
        jornadas.append(jornada_Seleccionada)
        new_Jornada_New=tk.StringVar()
        cmbx_Jornada_New = ttk.Combobox(frm_2, name="cmbx_jornada",state="readonly",
                                        values=jornadas,textvariable=new_Jornada_New)
        cmbx_Jornada_New.place(anchor="w",width=80, x=515, y=50)
        cmbx_Jornada_New.configure(state="disabled")
        
        #para cuando se cierra la ventana emergente se activa el interruptor
        #winEmergente.protocol("WM_DELETE_WINDOW", lambda: (interruptor.set(True),
                                                           #resultado.set("cerrar")))
        
        #============================================================================
        #Frame para botones
                                
        frm_3 = tk.Frame(winEmergente, name="frm_3")
        frm_3.configure(background="#f7f9fd", height=50, width=620)
        
        separator2 = ttk.Separator(frm_3)
        separator2.configure(orient="horizontal")
        separator2.place(anchor="nw", width=612, x=4, y=1)
        
        btnConfirmar=ttk.Button(frm_3, name="btnconfirmar")
        btnConfirmar.configure(text="Confirmar",command=lambda: (interruptor.set(True) if 
                                                                id_Curso_Select.get()!="" and new_Jornada_New.get()!="" else 
                                                                msg.showerror("Error","Por favor llene todos los campos"))
                                                                if checkbox_value.get() 
                                                                else ((interruptor.set(True) if 
                                                                new_Jornada.get()!="" else 
                                                                msg.showerror("Error","Por favor llene todos los campos"))))
        btnConfirmar.place(anchor="center",width=90 , x=210, y=25)
        
        btnCancelar=ttk.Button(frm_3, name="btncancelar")
        btnCancelar.configure(text="Cancelar", command=lambda: (interruptor.set(True),resultado.set("cerrar")))
        btnCancelar.place(anchor="center",width=90 , x=410, y=25)

        
        frm.pack()
        frm_2.pack()
        frm_3.pack()
        
        #Espera a que el interruptor se active para qeu continue la ejecucion
        winEmergente.wait_variable(interruptor)
        
        if resultado.get()!="cerrar":
            
            if checkbox_value.get():        
                winEmergente.destroy()
                return [id_Curso_Select.get(),new_Jornada_New.get()]
            
            else:
                winEmergente.destroy()
                return [new_Jornada.get()]
        else: 
            winEmergente.destroy()
            return
    def opciones(self, opcion):
        
        """La función opciones se encarga de establecer el comportamiento 
            de los botones de la ventana de inscripciones"""
        
        #Para que funcionen los botones, debe de haber un Alumno seleccionado
        if self.apellidos.get()!="" or self.nombres.get()!="":
            
            if opcion=="G":
                self.guardar_botton()
            elif opcion=="E":
                self.editar_botton()
            elif opcion=="D":
                self.delete_botton()
            elif opcion=="C":
                self.cancelar_botton()
            elif opcion=="S":
                self.cargar_tV()
        else:
            msg.showerror(title="¡Atención!",message="¡Ingrese un Alumno!")

    
    
    
if __name__ == "__main__":
    app = Inscripciones()
    app.run()