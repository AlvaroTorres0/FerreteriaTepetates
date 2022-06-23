import tkinter
from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
from datetime import datetime
import mariadb
import random
import threading
import time
from OperacionesBD import operaciones
#Importamos las clases de VentanasProducto
from VentanasProducto import Agregar as agregar
from VentanasProducto import Buscar as buscar
from VentanasProducto import Modificar as modificar
from VentanasProducto import Eliminar as eliminar


class MenuPrincipal:
    def __init__(self,u,p):
        self.usuario = u
        self.password = p
        print("Entró al menú principal como: ",self.usuario)

        self.ventanaPrincipal = Tk()
        self.ventanaPrincipal.title("Menú Principal")
        self.ventanaPrincipal.geometry("500x400")
        self.ventanaPrincipal.configure(background="#000000")

        self.btnRegistrarVenta = Button(self.ventanaPrincipal, text="Registrar Venta",bg="#53295e",fg="#ffffff",font=("System", 14),width=25,height=2,command = self.llamarVentanaVenta)
        self.btnRegistrarVenta.place(x=125,y=30)

        self.btnRegistrarCompra = Button(self.ventanaPrincipal, text="Registrar Compra",bg="#e30052",fg="#ffffff",font=("System", 14),width=25,height=2)
        self.btnRegistrarCompra.place(x=125,y=100)

        self.btnProdutos=Button(self.ventanaPrincipal,text="Productos",bg="#008080",fg="#ffffff",font=("System", 12),width=15,command=self.llamarMenuProducto)
        self.btnProdutos.place(x=40,y=220)
        self.btnEmpleados=Button(self.ventanaPrincipal,text="Empleados",bg="#79a100",fg="#ffffff",font=("System", 12),width=15)
        self.btnEmpleados.place(x=303,y=220)
        self.btnProveedores=Button(self.ventanaPrincipal,text="Proveedores",bg="#ff8c00",fg="#ffffff",font=("System", 12),width=15)
        self.btnProveedores.place(x=40,y=290)
        self.btnClientes = Button(self.ventanaPrincipal, text="Clientes", bg="#084d6e", fg="#ffffff",font=("System", 12), width=15)
        self.btnClientes.place(x=303,y=290)

        self.ventanaPrincipal.mainloop()

    # Método para llamar la subventana de las opciones de Producto
    def llamarMenuProducto(self):
        self.nuevaVentanaMenuProducto=tkinter.Toplevel(self.ventanaPrincipal)
        self.nuevaVentanaMenuProducto.geometry("600x550")
        self.nuevaVentanaMenuProducto.configure(background="#0a0a0a")
        self.nuevaVentanaMenuProducto.title("Menú Producto")
        self.ventanaPrincipal.iconify() #Con esto minimizamos una ventana

        # Armamos todo el layout para después trabajar solo en la principal
        self.contenedor = Frame(self.nuevaVentanaMenuProducto)
        self.contenedor.configure(background="#191919", width=400, height=470)
        self.contenedor.place(x=99, y=40)

        self.pestananaAzulSuperior = Frame(self.nuevaVentanaMenuProducto)
        self.pestananaAzulSuperior.configure(background="#053246", width=600, height=40)
        self.pestananaAzulSuperior.place(x=0, y=0)

        self.pestananaAzulInferior = Frame(self.nuevaVentanaMenuProducto)
        self.pestananaAzulInferior.configure(background="#053246", width=600, height=40)
        self.pestananaAzulInferior.place(x=0, y=510)

        # Cargamos el logo
        imagenLogo = Image.open("Imagenes\\logo_blanco.png")
        imagenLogo = imagenLogo.resize((110, 110), Image.ANTIALIAS)
        # La mandamos a la clase para después pasarla a un label
        self.logo = ImageTk.PhotoImage(imagenLogo)

        # Creamos el label que la contendrá
        self.lblLogo = Label(self.contenedor, image=self.logo, bg="#191919")
        self.lblLogo.place(x=70, y=30)

        SubMenuProducto(self.nuevaVentanaMenuProducto,self.usuario,self.password)

    def llamarVentanaVenta(self):
        self.nuevaVentanaVenta = tkinter.Toplevel(self.ventanaPrincipal)
        self.nuevaVentanaVenta.geometry("1400x750")
        self.nuevaVentanaVenta.configure(background="#0a0a0a")
        self.nuevaVentanaVenta.title("Nueva Venta")
        self.ventanaPrincipal.iconify()  # Con esto minimizamos una ventana

        # Armamos todo el layout para después trabajar solo en la principal
        self.contenedor = Frame(self.nuevaVentanaVenta)
        self.contenedor.configure(background="#191919", width=1400, height=750)
        self.contenedor.place(x=0, y=40)

        self.pestananaAzulSuperior = Frame(self.nuevaVentanaVenta)
        self.pestananaAzulSuperior.configure(background="#053246", width=1500, height=40)
        self.pestananaAzulSuperior.place(x=0, y=0)

        self.pestananaAzulInferior = Frame(self.nuevaVentanaVenta)
        self.pestananaAzulInferior.configure(background="#053246", width=1500, height=40)
        self.pestananaAzulInferior.place(x=0, y=710)

        # Cargamos el logo
        imagenLogo = Image.open("Imagenes\\logo_blanco.png")
        imagenLogo = imagenLogo.resize((110, 110), Image.ANTIALIAS)
        # La mandamos a la clase para después pasarla a un label
        self.logo = ImageTk.PhotoImage(imagenLogo)

        # Creamos el label que la contendrá
        self.lblLogo = Label(self.contenedor, image=self.logo, bg="#191919")
        self.lblLogo.place(x=1170, y=10)

        Venta(self.nuevaVentanaVenta, self.usuario, self.password)

class Venta:
    def __init__(self,ventana,u,p):

        self.operation = operaciones()
        #Se tiene que ir haciendo un pase de privilegios entre menús
        self.usuario = u
        self.password = p

        # Cambiamos los el nivel de permisos
        try:
            conn = mariadb.connect(user=u, password=p, host="localhost", database="ferreteriatepetates")
            self.cur = conn.cursor()
            print("Entró a la ventana Venta como: ", self.usuario)
        except mariadb.Error:
            print("Error en la conexión a Venta")

        #Iniciamos la transacción
        self.operation.iniciar(self.cur)

        self.ventanaPrincipal = ventana

        self.lblReferencia = Label(self.ventanaPrincipal, text="Nueva Venta", font=("Lucida Console", 16),bg="#053246",fg="#ffffff")
        self.lblReferencia.place(x=35,y=10)
        self.folio = str(self.generarFolio())
        self.lblFolio = Label(self.ventanaPrincipal, text=self.folio, bg="#1b2023",font=("Lucida Console", 14), fg="#ffffff")
        self.lblFolio.place(x=10, y=50)

        self.lblRFC = Label(self.ventanaPrincipal, text="RFC del cliente: ", bg="#1b2023",font=("Lucida Console", 14), fg="#ffffff")
        self.lblRFC.place(x=150, y=100)
        self.entryRFC = Entry(self.ventanaPrincipal, width=15, font=("Courier", 13), bg="#1b2023",fg="#ffffff")
        self.entryRFC.place(x=400, y=100)

        self.lblFecha = Label(self.ventanaPrincipal, text="Fecha de la venta: ", bg="#1b2023", font=("Lucida Console", 14),fg="#ffffff")
        self.lblFecha.place(x=700, y=100)
        self.entryFecha = Entry(self.ventanaPrincipal, width=22, font=("Courier", 13), bg="#1b2023", fg="#ffffff")
        self.entryFecha.place(x=930, y=100)

        self.fecha_hora = threading.Thread(target=self.actualizarHora)
        self.fecha_hora.start()

        self.lblNumeroEmpleado = Label(self.ventanaPrincipal, text="Número del empleado: ", bg="#1b2023", font=("Lucida Console", 14),fg="#ffffff")
        self.lblNumeroEmpleado.place(x=150, y=150)
        self.entryNumeroEmpleado = Entry(self.ventanaPrincipal, width=15, font=("Courier", 13), bg="#1b2023", fg="#ffffff")
        self.entryNumeroEmpleado.place(x=400, y=150)

        self.lblCodigoProd = Label(self.ventanaPrincipal, text="Código del producto: ", bg="#1b2023", font=("Lucida Console", 14),fg="#ffffff")
        self.lblCodigoProd.place(x=150, y=200)
        self.entryCodigoProd = Entry(self.ventanaPrincipal, width=15, font=("Courier", 13), bg="#1b2023", fg="#ffffff")
        self.entryCodigoProd.place(x=400, y=200)

        self.lblCantidad = Label(self.ventanaPrincipal, text="Cantidad: ", bg="#1b2023",font=("Lucida Console", 14), fg="#ffffff")
        self.lblCantidad.place(x=150, y=250)
        self.entryCantidad = Entry(self.ventanaPrincipal, width=15, font=("Courier", 13), bg="#1b2023", fg="#ffffff")
        self.entryCantidad.place(x=400, y=250)

        self.btnAgregar = Button(self.ventanaPrincipal, text="Agregar", bg="#5c1b6c", fg="#ffffff",font=("Lucida Console", 14), width=15,command=self.agregarTabla)
        self.btnAgregar.place(x=600, y=200)

        self.btnRegistrar = Button(self.ventanaPrincipal, text="Registrar", bg="#228b22", fg="#ffffff",font=("Lucida Console", 14), width=15, command=self.confirmarVenta)
        self.btnRegistrar.place(x=800, y=600)

        self.btnCancelar = Button(self.ventanaPrincipal, text="Cancelar", bg="#ff0000", fg="#ffffff",font=("Lucida Console", 14), width=15, command=self.cancelarVenta)
        self.btnCancelar.place(x=1100, y=600)

        self.tabla = ttk.Treeview(self.ventanaPrincipal,columns=("Nombre","Precio","Cantidad","Total","Marca","Puntos"))
        self.tabla.place(x=10,y=300)


        #Asignamos los encabezados de la tabla
        self.tabla.heading("#0",text="Codigo")
        self.tabla.heading("Nombre", text="Nombre")
        self.tabla.heading("Precio", text="Precio")
        self.tabla.heading("Cantidad", text="Cantidad")
        self.tabla.heading("Total", text="Total")
        self.tabla.heading("Marca", text="Marca")
        self.tabla.heading("Puntos", text="Puntos")

    #Armamos el arreglo que contendrá los datos de la venta
    def registrar(self):
        l = []
        l.append(self.folio)
        l.append(self.entryRFC.get())
        l.append(self.entryCodigoProd.get())
        l.append(self.entryNumeroEmpleado.get())
        l.append(self.entryCantidad.get())
        total = self.calcularTotal()
        l.append(total)
        l.append(self.entryFecha.get())

        return l

    #Agregamos filas a la tabla
    def agregarTabla(self):
        codigo = self.entryCodigoProd.get()
        rfc = self.entryRFC.get()


        #Agregamos a la tabla
        datos = self.operation.buscarParaTabla(self.cur,codigo)
        total = self.calcularTotal()
        cantidad = self.entryCantidad.get()
        # Agregamos a la base de datos
        self.agregarBD(rfc,codigo,cantidad)
        # Borramos las entradas
        self.entryCodigoProd.delete(0,"end")
        self.entryCantidad.delete(0,"end")

        codigo = datos[0]
        nombre = datos[1]
        precio = datos[2]
        marca = datos[3]
        puntos = datos[4]
        #Añadimos la columna
        self.tabla.insert("", END, text=str(codigo), values=(nombre, precio, cantidad, total, marca, puntos))


    #Agregamos la venta a la bd
    def agregarBD(self,rfc,codigo,cantidad):
        valores = self.registrar()
        #Registramos la venta
        self.operation.insertarVenta(self.cur,valores)
        #Actualizamos los puntos del cliente
        self.operation.sumarPuntosCliente(self.cur,rfc,codigo,cantidad)

    #Calculamos el total para la factura, precio * cantidad
    def calcularTotal(self):
        codigo = self.entryCodigoProd.get()
        precio = self.operation.buscarPrecio(self.cur,codigo)
        total = int(self.entryCantidad.get()) * float(precio[0])

        return total

    def generarFolio(self):
        folio = random.randint(00000000,99999999)
        return folio

    def confirmarVenta(self):
        self.operation.confirmar(self.cur)
        self.ventanaPrincipal.destroy()

    def cancelarVenta(self):
        self.operation.cancelar(self.cur)
        self.ventanaPrincipal.destroy()

    def actualizarHora(self):
        while True:
            self.fecha = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
            self.entryFecha.insert(0, self.fecha)
            time.sleep(1)
            self.entryFecha.delete(0, END)

class SubMenuProducto:
    def __init__(self,ventana,u,p):
        #Se tiene que ir haciendo un pase de privilegios entre menús
        self.usuario = u
        self.password = p
        print("Entró al Menu producto como: ",self.usuario)

        self.ventanaPrincipal = ventana

        self.lblReferencia = Label(self.ventanaPrincipal, text="Productos", font=("Lucida Console", 16),bg="#053246",fg="#ffffff")
        self.lblReferencia.place(x=35,y=10)

        self.btnAgregar = Button(self.ventanaPrincipal, text="Agregar Producto", bg="#191919", fg="#ffffff",font=("Lucida Console", 14),width=25,command = self.llamarVentanaAgregar)
        self.btnAgregar.place(x=160, y=200)
        self.btnBuscar = Button(self.ventanaPrincipal, text="Buscar Producto", bg="#191919", fg="#ffffff",font=("Lucida Console", 14),width=25,command = self.llamarVentanaBuscar)
        self.btnBuscar.place(x=160, y=270)
        self.btnModificar = Button(self.ventanaPrincipal, text="Modificar Producto", bg="#191919", fg="#ffffff", font=("Lucida Console", 14),width=25,command = self.llamarVentanaModificar)
        self.btnModificar.place(x=160, y=340)
        self.btnEliminar = Button(self.ventanaPrincipal, text="Eliminar Producto", bg="#191919", fg="#ffffff",font=("Lucida Console", 14),width=25,command = self.llamarVentanaEliminar)
        self.btnEliminar.place(x=160, y=410)

    # Método para armar y llamar la Ventana para agregar Producto
    def llamarVentanaAgregar(self):
        self.nuevaVentanaAgregar=tkinter.Toplevel(self.ventanaPrincipal)
        self.nuevaVentanaAgregar.title("Agregar Producto")
        self.nuevaVentanaAgregar.geometry("690x900")
        self.nuevaVentanaAgregar.configure(background="#1b2023")
        agregar(self.nuevaVentanaAgregar,self.usuario,self.password)

    def llamarVentanaBuscar(self):
        self.nuevaVentanaBuscar = tkinter.Toplevel(self.ventanaPrincipal)
        self.nuevaVentanaBuscar.title("Buscar Producto")
        self.nuevaVentanaBuscar.geometry("600x400")
        self.nuevaVentanaBuscar.configure(background="#1b2023")
        buscar(self.nuevaVentanaBuscar,self.usuario,self.password)

    def llamarVentanaModificar(self):
        self.nuevaVentanaModificar = tkinter.Toplevel(self.ventanaPrincipal)
        self.nuevaVentanaModificar.title("Modificar Producto")
        self.nuevaVentanaModificar.geometry("690x900")
        self.nuevaVentanaModificar.configure(background="#1b2023")
        modificar(self.nuevaVentanaModificar)

    def llamarVentanaEliminar(self):
        self.nuevaVentanaEliminar = tkinter.Toplevel(self.ventanaPrincipal)
        self.nuevaVentanaEliminar.title("Eliminar Producto")
        self.nuevaVentanaEliminar.geometry("500x200")
        self.nuevaVentanaEliminar.configure(background="#1b2023")
        eliminar(self.nuevaVentanaEliminar,self.usuario,self.password)