from tkinter import *
from PIL import ImageTk, Image
from tkinter import filedialog
import mariadb
from OperacionesBD import operaciones
from tkinter import messagebox


operation = operaciones()

class Agregar:
    def __init__(self,ventana,u,p):
        try:
            self.conn = mariadb.connect(user=u, password=p, host="localhost", database="ferreteriatepetates")
            self.cur = self.conn.cursor()
            print("Agregar, nivel de privilegios: ",u)
        except mariadb.Error:
            print("Error")

        self.ventanaPrincipal = ventana

        self.lblReferencia = Label(self.ventanaPrincipal,text="Nuevo Producto", bg="#1b2023",font=("Lucida Console", 20),fg="#ffffff")
        self.lblReferencia.pack()

        self.lblCodigoBarras = Label(self.ventanaPrincipal,text="Código de Barras: ",bg="#1b2023",font=("Lucida Console", 14),fg="#ffffff")
        self.lblCodigoBarras.place(x=20,y=80)
        self.entryCodigoBarras = Entry(self.ventanaPrincipal,width=15,font=("Courier", 13),bg="#1b2023",fg="#ffffff")
        self.entryCodigoBarras.place(x=310,y=80)
        self.btnCapturarCodigoBarras = Button(self.ventanaPrincipal,text="Capturar Código",font=("System", 14),bg="#461c50",fg="#ffffff")
        self.btnCapturarCodigoBarras.place(x=490,y=70)

        self.lblNombreProducto = Label(self.ventanaPrincipal, text="Nombre del Producto: ", bg="#1b2023",font=("Lucida Console", 14), fg="#ffffff")
        self.lblNombreProducto.place(x=20, y=145)
        self.entryNombreProducto = Entry(self.ventanaPrincipal, width=35,font=("Courier", 13),bg="#1b2023",fg="#ffffff")
        self.entryNombreProducto.place(x=310, y=145)

        self.lblDescripcion = Label(self.ventanaPrincipal, text="Descripción del Producto: ", bg="#1b2023",font=("Lucida Console", 14), fg="#ffffff")
        self.lblDescripcion.place(x=20, y=205)
        self.cajaDescripcion = Text(self.ventanaPrincipal, width=35, height=5,font=("Courier", 13),bg="#1b2023",fg="#ffffff")
        self.cajaDescripcion.place(x=310, y=205)

        self.lblPrecio = Label(self.ventanaPrincipal, text="Precio Unitario: ", bg="#1b2023",font=("Lucida Console", 14), fg="#ffffff")
        self.lblPrecio.place(x=20, y=345)
        self.entryPrecio = Entry(self.ventanaPrincipal, width=35,font=("Courier", 13),bg="#1b2023",fg="#ffffff")
        self.entryPrecio.place(x=310, y=345)

        self.lblExistencia = Label(self.ventanaPrincipal, text="Cantidad de Unidades: ", bg="#1b2023",font=("Lucida Console", 14), fg="#ffffff")
        self.lblExistencia.place(x=20, y=405)
        self.entryExistencia = Entry(self.ventanaPrincipal, width=35,font=("Courier", 13),bg="#1b2023",fg="#ffffff")
        self.entryExistencia.place(x=310, y=405)

        self.lblCategoria = Label(self.ventanaPrincipal, text="Categoría del Producto: ", bg="#1b2023",font=("Lucida Console", 14), fg="#ffffff")
        self.lblCategoria.place(x=20, y=465)
        self.entryCategoria = Entry(self.ventanaPrincipal, width=35,font=("Courier", 13),bg="#1b2023",fg="#ffffff")
        self.entryCategoria.place(x=310, y=465)

        self.lblMarca = Label(self.ventanaPrincipal, text="Marca del Producto: ", bg="#1b2023",font=("Lucida Console", 14), fg="#ffffff")
        self.lblMarca.place(x=20, y=525)
        self.entryMarca = Entry(self.ventanaPrincipal, width=35,font=("Courier", 13),bg="#1b2023",fg="#ffffff")
        self.entryMarca.place(x=310, y=525)

        self.lblCosto = Label(self.ventanaPrincipal, text="Costo de Compra: ", bg="#1b2023",font=("Lucida Console", 14), fg="#ffffff")
        self.lblCosto.place(x=20, y=585)
        self.entryCosto = Entry(self.ventanaPrincipal, width=35,font=("Courier", 13),bg="#1b2023",fg="#ffffff")
        self.entryCosto.place(x=310, y=585)

        self.lblPuntosProducto = Label(self.ventanaPrincipal, text="Puntos por Compra: ", bg="#1b2023",font=("Lucida Console", 14), fg="#ffffff")
        self.lblPuntosProducto.place(x=20, y=645)
        self.entryPuntosProducto = Entry(self.ventanaPrincipal, width=35,font=("Courier", 13),bg="#1b2023",fg="#ffffff")
        self.entryPuntosProducto.place(x=310, y=645)

        self.btnCapturarImagen = Button(self.ventanaPrincipal, text="Seleccionar imagen", font=("System", 14),bg="#3f3f3f", fg="#ffffff",command=self.seleccionarImagen)
        self.btnCapturarImagen.place(x=20, y=725)

        self.btnRegistrarProducto = Button(self.ventanaPrincipal, text="Registrar", font=("System", 14),bg="#008000", fg="#ffffff",command = self.registrar)
        self.btnRegistrarProducto.place(x=420, y=750)

        self.btnCancelarRegistro = Button(self.ventanaPrincipal, text="Cancelar", font=("System", 16),bg="#ff0000", fg="#ffffff",command=self.cancelarRegistro)
        self.btnCancelarRegistro.place(x=570, y=750)

    def confirmar(self):
        self.conn.commit()

    def seleccionarImagen(self):
        self.imagen = filedialog.askopenfilename(title="Seleccionar Imagen")
        imagenLogo = Image.open(self.imagen)
        imagenLogo = imagenLogo.resize((130, 130), Image.ANTIALIAS)
        self.logo = ImageTk.PhotoImage(imagenLogo)
        self.lblImagenProducto = Label(self.ventanaPrincipal, image=self.logo, bg="#ec5353")
        self.lblImagenProducto.place(x=200, y=725)

    def cancelarRegistro(self):
        self.ventanaPrincipal.destroy()

    def registrar(self):
        l = []
        l.append(self.entryCodigoBarras.get())
        l.append(self.entryNombreProducto.get())
        l.append(self.cajaDescripcion.get("1.0","end"))
        l.append(float(self.entryPrecio.get()))
        l.append(str(self.imagen))
        l.append(int(self.entryExistencia.get()))
        l.append(self.entryCategoria.get())
        l.append(self.entryMarca.get())
        l.append(1)
        l.append(float(self.entryCosto.get()))
        l.append(int(self.entryPuntosProducto.get()))

        operation.insertarDatos(self.cur,l)
        self.confirmar()
        self.ventanaPrincipal.withdraw()

class Buscar:
    def __init__(self, ventana,u,p):
        try:
            self.conn = mariadb.connect(user=u, password=p, host="localhost", database="ferreteriatepetates")
            self.cur = self.conn.cursor()
            print("Buscar, nivel de privilegios: ",u)
        except mariadb.Error:
            print("mamó el otro")

        self.ventanaPrincipal = ventana

        self.lblMostrar = Label(self.ventanaPrincipal,text="Buscar Productos",bg="#1b2023",font=("Lucida Console", 20),fg="#ffffff")
        self.lblMostrar.pack()

        self.var = IntVar()
        self.radioNombre = Radiobutton(self.ventanaPrincipal,text="Buscar por nombre",variable=self.var,value=1,bg="#1b2023",font=("Lucida Console", 14),fg="#ffffff",selectcolor="Black")
        self.radioNombre.place(x=20,y=45)
        self.radioCodigo = Radiobutton(self.ventanaPrincipal, text="Buscar por código", variable=self.var, value=2,bg="#1b2023",font=("Lucida Console", 14),fg="#ffffff",selectcolor="Black")
        self.radioCodigo.place(x=20,y=75)
        self.radioCategoria = Radiobutton(self.ventanaPrincipal, text="Buscar por categoría", variable=self.var, value=3,bg="#1b2023",font=("Lucida Console", 14),fg="#ffffff",selectcolor="Black")
        self.radioCategoria.place(x=20,y=105)

        self.btnCapturarCodigo = Button(self.ventanaPrincipal, text="Capturar código de barras", font=("System", 14), bg="#461c50", fg="#ffffff")
        self.btnCapturarCodigo.place(x=350, y=75)

        self.EntryBuscar = Entry(self.ventanaPrincipal,width=40,font=("Courier", 13),bg="#1b2023",fg="#ffffff",justify=CENTER)
        self.EntryBuscar.place(x=20, y=165)

        self.bntBuscar = Button(self.ventanaPrincipal,text = "Buscar",font=("System", 14),bg="#008000", fg="#ffffff",command=self.mostrarDatos)
        self.bntBuscar.place(x=450, y=165)

        self.cajadeTexto = Text(self.ventanaPrincipal,width=58, height=5,font=("Courier", 13),bg="#1b2023",fg="#ffffff")
        self.cajadeTexto.place(x=8,y=240)

    def mostrarDatos(self):
        tipodeBusqueda = self.var.get()
        datoBusqueda = self.EntryBuscar.get()
        # Limpiamos la caja de búsqueda
        self.cajadeTexto.delete("1.0", "end")
        if tipodeBusqueda == 1:
            datos = operation.buscar(self.cur, 'nombre_p', datoBusqueda)
            for i in datos:
                self.cajadeTexto.insert("insert", str(i))
                self.cajadeTexto.insert("insert", str("\n"))
        if tipodeBusqueda == 2:
            datos = operation.buscar(self.cur, "codigo_p", datoBusqueda)
            for i in datos:
                self.cajadeTexto.insert("insert", str(i))
                self.cajadeTexto.insert("insert", str("\n"))
        if tipodeBusqueda == 3:
            datos = operation.buscar(self.cur, "categoria", datoBusqueda)
            for i in datos:
                self.cajadeTexto.insert("insert", str(i))
                self.cajadeTexto.insert("insert", str("\n"))

class Modificar:
    def __init__(self,ventana):
        self.ventanaPrincipal = ventana

        self.lblReferencia = Label(self.ventanaPrincipal, text="Modificar datos de un producto", bg="#1b2023",font=("Lucida Console", 20), fg="#ffffff")
        self.lblReferencia.pack()

        self.lblCodigoBarras = Label(self.ventanaPrincipal, text="Código del producto: ", bg="#1b2023",font=("Lucida Console", 14), fg="#ffffff")
        self.lblCodigoBarras.place(x=20, y=80)
        self.entryCodigoBarras = Entry(self.ventanaPrincipal, width=15, font=("Courier", 13), bg="#1b2023",fg="#ffffff")
        self.entryCodigoBarras.place(x=310, y=80)
        self.btnBuscar = Button(self.ventanaPrincipal, text="Buscar producto", font=("System", 14),bg="#461c50", fg="#ffffff")
        self.btnBuscar.place(x=490, y=70)

        self.lblNombreProducto = Label(self.ventanaPrincipal, text="Nombre del Producto: ", bg="#1b2023", font=("Lucida Console", 14), fg="#ffffff")
        self.lblNombreProducto.place(x=20, y=145)
        self.entryNombreProducto = Entry(self.ventanaPrincipal, width=35, font=("Courier", 13), bg="#1b2023",fg="#ffffff")
        self.entryNombreProducto.place(x=310, y=145)

        self.lblDescripcion = Label(self.ventanaPrincipal, text="Descripción del Producto: ", bg="#1b2023",font=("Lucida Console", 14), fg="#ffffff")
        self.lblDescripcion.place(x=20, y=205)
        self.cajaDescripcion = Text(self.ventanaPrincipal, width=35, height=5, font=("Courier", 13), bg="#1b2023",fg="#ffffff")
        self.cajaDescripcion.place(x=310, y=205)

        self.lblPrecio = Label(self.ventanaPrincipal, text="Precio Unitario: ", bg="#1b2023",font=("Lucida Console", 14), fg="#ffffff")
        self.lblPrecio.place(x=20, y=345)
        self.entryPrecio = Entry(self.ventanaPrincipal, width=35, font=("Courier", 13), bg="#1b2023", fg="#ffffff")
        self.entryPrecio.place(x=310, y=345)

        self.lblExistencia = Label(self.ventanaPrincipal, text="Cantidad de Unidades: ", bg="#1b2023",font=("Lucida Console", 14), fg="#ffffff")
        self.lblExistencia.place(x=20, y=405)
        self.entryExistencia = Entry(self.ventanaPrincipal, width=35, font=("Courier", 13), bg="#1b2023", fg="#ffffff")
        self.entryExistencia.place(x=310, y=405)

        self.lblCategoria = Label(self.ventanaPrincipal, text="Categoría del Producto: ", bg="#1b2023",font=("Lucida Console", 14), fg="#ffffff")
        self.lblCategoria.place(x=20, y=465)
        self.entryCategoria = Entry(self.ventanaPrincipal, width=35, font=("Courier", 13), bg="#1b2023", fg="#ffffff")
        self.entryCategoria.place(x=310, y=465)

        self.lblMarca = Label(self.ventanaPrincipal, text="Marca del Producto: ", bg="#1b2023",font=("Lucida Console", 14), fg="#ffffff")
        self.lblMarca.place(x=20, y=525)
        self.entryMarca = Entry(self.ventanaPrincipal, width=35, font=("Courier", 13), bg="#1b2023", fg="#ffffff")
        self.entryMarca.place(x=310, y=525)

        self.lblCosto = Label(self.ventanaPrincipal, text="Costo de Compra: ", bg="#1b2023",font=("Lucida Console", 14), fg="#ffffff")
        self.lblCosto.place(x=20, y=585)
        self.entryCosto = Entry(self.ventanaPrincipal, width=35, font=("Courier", 13), bg="#1b2023", fg="#ffffff")
        self.entryCosto.place(x=310, y=585)

        self.lblPuntosProducto = Label(self.ventanaPrincipal, text="Puntos por Compra: ", bg="#1b2023",font=("Lucida Console", 14), fg="#ffffff")
        self.lblPuntosProducto.place(x=20, y=645)
        self.entryPuntosProducto = Entry(self.ventanaPrincipal, width=35, font=("Courier", 13), bg="#1b2023",fg="#ffffff")
        self.entryPuntosProducto.place(x=310, y=645)

        self.btnCapturarImagen = Button(self.ventanaPrincipal, text="Seleccionar nueva imagen", font=("System", 14),bg="#3f3f3f", fg="#ffffff", command=self.seleccionarImagen)
        self.btnCapturarImagen.place(x=20, y=725)

        self.btnModificarProducto = Button(self.ventanaPrincipal, text="Modificar", font=("System", 14), bg="#008000",fg="#ffffff")
        self.btnModificarProducto.place(x=430, y=750)

        self.btnCancelar = Button(self.ventanaPrincipal, text="Cancelar", font=("System", 16), bg="#ff0000", fg="#ffffff", command=self.cancelarRegistro)
        self.btnCancelar.place(x=580, y=750)


    def seleccionarImagen(self):
        imagen = filedialog.askopenfilename(title="Seleccionar Imagen")
        print(imagen)
        imagenLogo = Image.open(imagen)
        imagenLogo = imagenLogo.resize((130, 130), Image.ANTIALIAS)
        self.logo = ImageTk.PhotoImage(imagenLogo)
        self.lblImagenProducto = Label(self.ventanaPrincipal, image=self.logo, bg="#ec5353")
        self.lblImagenProducto.place(x=250, y=725)

    def cancelarRegistro(self):
        self.ventanaPrincipal.destroy()


    def crearListaNuevosValores(self):
        self.nuevosValores = []
        self.nuevosValores.append(self.EntryClave.get())
        self.nuevosValores.append(self.EntryNombre.get())
        self.nuevosValores.append(self.EntryCompuesto.get())
        self.nuevosValores.append(self.EntryFechaCad.get())
        self.nuevosValores.append(self.EntryCantidad.get())
        self.nuevosValores.append(self.EntryPrecio.get())

        self.modificar()

    def modificar(self):
        operation.modificarDatosCompletos(cursor,self.nuevosValores)
        connect.confirmar()
        self.ventanaPrincipal.withdraw()

class Eliminar:
    def __init__(self,ventana,u,p):
        try:
            self.conn = mariadb.connect(user=u, password=p, host="localhost", database="ferreteriatepetates")
            self.cur = self.conn.cursor()
            print("Eliminar, nivel de privilegios: ",u)
        except mariadb.Error:
            print("mamó el otro")

        self.ventanaPrincipal = ventana

        self.label1 = Label(self.ventanaPrincipal,text="Eliminar productos",bg="#1b2023",font=("Lucida Console", 20),fg="#ffffff")
        self.label1.pack()

        self.lblClaveEliminar = Label(self.ventanaPrincipal,text="Digita clave del producto a eliminar",bg="#1b2023",font=("Lucida Console", 14), fg="#ffffff")
        self.lblClaveEliminar.place(x=50,y=50)

        self.EntryEliminar = Entry(self.ventanaPrincipal,width=14, font=("Courier", 13), bg="#1b2023",fg="#ffffff",justify=CENTER)
        self.EntryEliminar.place(x=100,y=95)

        self.btnEliminar = Button(self.ventanaPrincipal,text="Eliminar",font=("System", 16), bg="#ff0000", fg="#ffffff",command=self.confirmarEliminacion)
        self.btnEliminar.place(x=300,y=95)

    def confirmarEliminacion(self):
        codigoProd = self.EntryEliminar.get()
        registroEncontrado = operation.buscarPorClave(self.cur,codigoProd)

        if registroEncontrado=="":
            messagebox.showinfo(title="No encontrado", message="Producto no encontrado" )

        elif registroEncontrado!="":
            messagebox.showinfo(title="Datos del Producto", message="El producto es: "+str(registroEncontrado))
            respuesta = messagebox.askyesno(title="Eliminar", message="¿Desea eliminarlo?")

            if respuesta:
                self.eliminar(codigoProd)
            else:
                self.ventanaPrincipal.withdraw()

    def eliminar(self,clave):
        operation.eliminarDatos(self.cur,clave)
        self.ventanaPrincipal.withdraw()