from tkinter import *
from PIL import ImageTk, Image
from tkinter import messagebox
from OperacionesBD import operaciones
from Menu import MenuPrincipal as mp
import mariadb


def conexion(u,p,h,db):
    #Pasamos la conexion
    try:
        conn = mariadb.connect(user=u,password=p,host=h,database=db)
        print("Conexión Exitosa")
    except mariadb.Error:
        print("Error en Conexión")
    return conn


operation = operaciones()
conn = conexion("root","sisekersuren","localhost","ferreteriatepetates")
cur = conn.cursor()

class Principal:
    def __init__(self):
        self.ventanaLogin = Tk()
        self.ventanaLogin.title("Login")
        self.ventanaLogin.geometry("750x500")

        self.mitad1 = Frame(self.ventanaLogin)
        self.mitad1.configure(background="#ec5353",width=375,height=500)
        self.mitad1.place(x=0,y=0)

        self.mitad2 = Frame(self.ventanaLogin)
        self.mitad2.configure(background="#00304E", width=375,height=500)
        self.mitad2.place(x=375,y=0)

        # PRIMERA MITAD DE LA VENTANA
        # Cargamos el logo
        imagenLogo = Image.open("Imagenes\\logo.png")
        imagenLogo = imagenLogo.resize((130, 130), Image.ANTIALIAS)
        # La mandamos a la clase para después pasarla a un label
        self.logo = ImageTk.PhotoImage(imagenLogo)

        # Creamos el label que la contendrá
        self.lblLogo = Label(self.mitad1, image=self.logo, bg="#ec5353")
        self.lblLogo.place(x=115, y=220)

        # SEGUNDA MITAD DE LA VENTANA
        self.lblNumeroEmpleado = Label(self.mitad2,text="NÚMERO DE EMPLEADO",font=("System", 12),bg="#00304E",fg="#ffffff")
        self.lblNumeroEmpleado.place(x=90,y=120)
        self.entryNumeroEmpleado = Entry(self.mitad2,width=27,font=("Ubuntu Condensed", 14),bg="#00304E",fg="#ffffff",justify=CENTER)
        self.entryNumeroEmpleado.place(x=40,y=150)

        self.lblContrasena = Label(self.mitad2,text = "CONTRASEÑA",font=("System", 12),bg="#00304E",fg="#ffffff")
        self.lblContrasena.place(x=130,y=200)
        self.entryContrasena = Entry(self.mitad2,width=27,font=("Ubuntu Condensed", 14),bg="#00304E",fg="#ffffff",show="*",justify=CENTER)
        self.entryContrasena.place(x=40,y=230)

        self.btnIniciarSesion = Button(self.mitad2,text="Iniciar Sesión",font=("System",12),bg="#ec5353",fg="#ffffff",width=13,command = self.iniciarSesion)
        self.btnIniciarSesion.place(x=120,y=300)

        self.ventanaLogin.mainloop()

    def crearTupla(self,user, password):
        tupla = (user, password)
        return tupla

    def iniciarSesion(self):
        numeroempleado = self.entryNumeroEmpleado.get()
        contrasena = self.entryContrasena.get()

        tupla = self.crearTupla(numeroempleado,contrasena)

        #Aquí evaluamos si el usuario ingresó o no ya que nos devuelve True o False
        iniciado = operation.loginCuenta(conn,tupla)

        #Hacemos tupla para la consulta
        no_empleado = (self.entryNumeroEmpleado.get(),)
        cargo = operation.conocerUsuario(conn,no_empleado)

        if iniciado:
            #Hacemos la comparación del cargo
            if cargo [0]==("ENCARGADO DE ALMACEN",):
                self.ventanaLogin.destroy()
                menuPrincipal = mp("almacen","almacen")
            if cargo [0]==("CAJERO",):
                self.ventanaLogin.destroy()
                menuPrincipal = mp("cajero","cajero")
            if cargo [0]==("PROPIETARIO",):
                self.ventanaLogin.destroy()
                menuPrincipal = mp("propietario","propietario")
            cur.close()

        else:
            self.entryNumeroEmpleado.delete(0, END)
            self.entryContrasena.delete(0, END)
            messagebox.showerror(title="Error al iniciar",message="Usuario o contraseña incorrectos, por favor verifique")

login = Principal()