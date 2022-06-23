from tkinter import messagebox
class operaciones:
    def insertarDatos(self,cursor,datos):
        sql = "INSERT INTO producto(codigo_p,nombre_p,descripcion,precio,imagen,existencia,categoria,marca,estatus,costo,puntos_producto) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql,datos)
        messagebox.showinfo(title="Agregado", message="Producto agregado correctamente")

    def buscar(self,cursor,campo,dato):
        datos_producto=[]
        sql = "SELECT codigo_p,nombre_p,descripcion,precio,existencia,categoria,marca,estatus,puntos_producto FROM producto WHERE "+campo+"="+"'"+dato+"'"
        cursor.execute(sql)
        for i in cursor:
            datos_producto.append(i)
        return datos_producto

    def buscarPorClave(self,cursor,codigo_p):
        try:
            sql = "SELECT codigo_p,nombre_p,descripcion,precio,categoria,marca,estatus FROM producto WHERE codigo_p="+"'"+codigo_p+"'"
            cursor.execute(sql)
            for f in cursor:
                registro = f
            return registro
        except:
            return ""

    def eliminarDatos(self,cursor,codigo_p):
        sql = "DELETE FROM producto WHERE codigo_p="+"'"+codigo_p+"'"
        cursor.execute(sql)
        self.confirmar(cursor)
        messagebox.showinfo(title="Eliminado", message="Producto eliminado")

    def modificarDatosCompletos(self,cursor,nuevosvalores):
        clave = nuevosvalores[0]
        nuevoNombre = nuevosvalores[1]
        nuevoCompuesto = nuevosvalores[2]
        nuevaFechaCad = nuevosvalores[3]
        nuevaCantDisp = nuevosvalores[4]
        nuevoPrecio = nuevosvalores[5]
        sql1 = "UPDATE medicamento set nombre=" + "'" + nuevoNombre + "'" + " WHERE clave=" + "'" + clave + "'"
        sql2 = "UPDATE medicamento set compuesto=" + "'" + nuevoCompuesto + "'" + " WHERE clave=" + "'" + clave + "'"
        sql3 = "UPDATE medicamento set fechacad=" + "'" + nuevaFechaCad + "'" + " WHERE clave=" + "'" + clave + "'"
        sql4 = "UPDATE medicamento set cantdisp=" + "'" + nuevaCantDisp + "'" + " WHERE clave=" + "'" + clave + "'"
        sql5 = "UPDATE medicamento set precio=" + "'" + nuevoPrecio + "'" + " WHERE clave=" + "'" + clave + "'"

        cursor.execute(sql1)
        cursor.execute(sql2)
        cursor.execute(sql3)
        cursor.execute(sql4)
        cursor.execute(sql5)

        messagebox.showinfo(title="Modificado",message="Medicamento modificado correctamente")


    #Métodos transacción
    def iniciar(self,cursor):
        sql = "BEGIN"
        cursor.execute(sql)
        print("Transacción iniciada")

    def confirmar(self,cursor):
        sql = "COMMIT"
        cursor.execute(sql)
        messagebox.showinfo(title="Venta realizada", message="Venta realizada con éxito")

    def cancelar(self,cursor):
        sql = "ROLLBACK"
        cursor.execute(sql)

    def buscarParaTabla(self,cursor,codigo_p):
        try:
            sql = "SELECT codigo_p,nombre_p,precio,marca,puntos_producto FROM producto WHERE codigo_p="+"'"+codigo_p+"'"
            cursor.execute(sql)
            for f in cursor:
                registro = f
            return registro
        except:
            return ""

    def insertarVenta(self,cursor,datos):
        sql = "INSERT INTO venta(folio_venta,rfc_cliente_v,codigo_p_v,no_empleado_v,cantidad,total,fecha_v) VALUES(%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql,datos)

    def buscarPrecio(self,cursor,codigo_p):
        try:
            sql = "SELECT precio FROM producto WHERE codigo_p="+"'"+codigo_p+"'"
            cursor.execute(sql)
            for f in cursor:
                registro = f

            return registro
        except:
            return ""

    def sumarPuntosCliente(self,cursor,rfc,producto,cantidad):
        sql = "UPDATE cliente SET puntos = puntos + (SELECT puntos_producto FROM producto WHERE codigo_p = "+"'"+producto+"'"+") * "+cantidad+" WHERE rfc_cliente = "+"'"+rfc+"'"
        cursor.execute(sql)

    #Métodos para logeo
    def conocerUsuario(self,conn,empleado):
        cur = conn.cursor()
        datos_empleado = []
        sql = "SELECT cargo FROM empleado WHERE no_empleado=%s"
        cur.execute(sql, empleado)
        for i in cur:
            datos_empleado.append(i)
        return datos_empleado

    def loginCuenta(self,conn,datos):
        cur = conn.cursor()
        sql = "SELECT * FROM empleado WHERE no_empleado=%s AND contrasena=%s"
        cur.execute(sql,datos)

        if cur.fetchone():
            cur.close()
            return True
        else:
            return False