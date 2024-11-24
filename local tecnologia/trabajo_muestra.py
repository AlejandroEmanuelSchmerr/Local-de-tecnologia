from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from turtle import width
import mysql.connector
global conexion

def conectar_bd():
        conexion = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            database="tecnologias"
        )
        cursor = conexion.cursor                                    ()
        return conexion
    


# Variables globales
datos_productos = []
datos_clientes = []
resultados_treeview = None
marca = None
tabla = None
cuadro_filtro = None
tabla2 = None
dni = None
seleccion_id = None
def ventana_productos():
    ventana_productos=Toplevel(ventana)
    ventana_productos.geometry("700x400")
    ventana_productos.config(bg="blue")
    ventana_productos.title("Ventana Principal Productos")



    cargar = Button(ventana_productos, text='Cargar Producto',font=10,height=2, command=carga_datos)
    cargar.place(x=0,y=345)
    bym = Button(ventana_productos, text='Baja y Modificación de Producto',font=10,height=2, command=bm)
    bym.place(x=200,y=345)
    fl = Button(ventana_productos, text='Filtracion de Producto',font=10,height=2, command=filtracion)
    fl.place(x=500,y=345)
    imagen_etiqueta_pr = Label(ventana_productos,image=fotos7)
    imagen_etiqueta_pr.place(x=50, y=0)    
    
    
def filtracion():
    global resultados_treeview
    global cuadro_filtro
    global marca
    
    filtracion = Toplevel()
    filtracion.geometry('850x300')
    filtracion.title("Ventana de Filtración")
    filtracion.config(bg='MediumPurple1')
    etiqueta_filtro = Label(filtracion, text="Filtrar por Marca de Producto")
    etiqueta_filtro.grid(row=0, column=0, padx=5, pady=5)
    marca = StringVar()
    cuadro_filtro = Entry(filtracion, textvariable=marca, width=50)
    cuadro_filtro.grid(row=0, column=1, padx=5, pady=5)
    boton_filtrar = Button(filtracion, text="Filtrar", command=filtrar_productos)
    boton_filtrar.grid(row=1, column=0, padx=5, pady=5)
    
    boton_filtrar.config(command=filtrar_productos)
    
    resultados_treeview = ttk.Treeview(filtracion, columns=( "Producto", "Modelo", "Marca", "Precio", "Descripción", "Stock"))
    resultados_treeview.grid(row=5, column=0, columnspan=4)
    resultados_treeview.column("#0", width=0, stretch=NO)
    resultados_treeview.heading("Producto", text="Producto", anchor=CENTER)
    resultados_treeview.heading("Modelo", text="Modelo", anchor=CENTER)
    resultados_treeview.heading("Marca", text="Marca", anchor=CENTER)
    resultados_treeview.heading("Precio", text="Precio", anchor=CENTER)
    resultados_treeview.heading("Descripción", text="Descripción", anchor=CENTER)
    resultados_treeview.heading("Stock", text="Stock", anchor=CENTER)
    resultados_treeview.column("Producto", width=150)
    resultados_treeview.column("Modelo", width=150)
    resultados_treeview.column("Marca", width=100)
    resultados_treeview.column("Precio", width=100)
    resultados_treeview.column("Descripción", width=200)
    resultados_treeview.column("Stock", width=100)

    
def filtrar_productos():
    global resultados_treeview
    global marca
    marca_filtrar = marca.get()

    if resultados_treeview:
        resultados_treeview.delete(*resultados_treeview.get_children())  

    if marca_filtrar:
        db = conectar_bd()
        cursor = db.cursor()
        cursor.execute("SELECT producto, modelo, marca, precio, descripcion, stock FROM productos WHERE marca = %s", (marca_filtrar,))
        resultados = cursor.fetchall()
        db.close()
        
        for producto, modelo, marca, precio, descripcion, stock in resultados:
            resultados_treeview.insert("", "end", values=(producto, modelo, marca, precio, descripcion, stock))






def bm():
    global datos_productos
    marca_var = StringVar()
    producto_a_modificar = StringVar()
    modelo_a_modificar = StringVar()
    precio_a_modificar = DoubleVar()
    descripcion_a_modificar = StringVar()
    stock_a_modificar = StringVar()

    def buscar_por_marca():
        marca = marca_var.get()
        db = conectar_bd()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM productos WHERE marca = %s", (marca,))
        productos = cursor.fetchall()
        db.close()

        if productos:
            mensaje = "Productos encontrados:\n"
            for producto in productos:
                mensaje += f"Marca: {producto[3]}, Producto: {producto[1]}, Modelo: {producto[2]}, Precio: {producto[4]}\n,Descripcion :{producto[5]}/n,Stock : {producto[6]} "
            messagebox.showinfo("Resultados de búsqueda", mensaje)
        else:
            messagebox.showinfo("Resultados de búsqueda", "No se encontraron productos con esa marca.")

    def modificar():
        global datos_productos
        global tabla
        global resultados_treeview
        nueva_marca = marca_var.get()
        nuevo_producto = producto_a_modificar.get()
        nuevo_modelo = modelo_a_modificar.get()
        nuevo_precio = precio_a_modificar.get()
        nueva_descripcion = descripcion_a_modificar.get()
        nuevo_stock = stock_a_modificar.get()

        db = conectar_bd()
        cursor = db.cursor()
        cursor.execute("UPDATE productos SET producto=%s, modelo=%s, precio=%s, descripcion=%s, stock=%s WHERE marca=%s", 
                      (nuevo_producto, nuevo_modelo, nuevo_precio, nueva_descripcion, nuevo_stock, nueva_marca))
        db.commit()
        db.close()
        for i, (producto,modelo,marca,precio,descripcion,stock) in enumerate(datos_productos):
                if marca == nueva_marca:
                    datos_productos[i] = (nuevo_producto, nuevo_modelo,marca, nuevo_precio,nueva_descripcion,nuevo_stock)
                    break
        actualizar_grilla_productos()
        actualizar_grilla_filtracion()
        messagebox.showinfo("Modificación", "El producto ha sido modificado con éxito.")

    def dar_de_baja():
        global tabla
        global resultados_treeview
        global datos_productos
        marca = marca_var.get()
        db = conectar_bd()
        cursor = db.cursor()
        cursor.execute("DELETE FROM productos WHERE marca = %s", (marca,))
        db.commit()
        db.close()
        for i, (producto, modelo, marca, precio, descripcion, stock) in enumerate(datos_productos):
                if marca == marca_var:
                    datos_productos.pop(i)
                    break
        actualizar_grilla_productos()
        actualizar_grilla_filtracion()
        messagebox.showinfo("Dar de Baja", "El producto ha sido dado de baja con éxito.")


    def actualizar_grilla_productos():
        global tabla
        global datos_productos
        
        if tabla:
            for item in tabla.get_children():
                tabla.delete(item)
            for producto, modelo, marca, precio, descripcion, stock in datos_productos:
                tabla.insert("", "end", values=(producto, modelo, marca, precio, descripcion, stock))
    def actualizar_grilla_filtracion():
        global resultados_treeview
        global datos_productos

        if resultados_treeview:
            for item in resultados_treeview.get_children():
                resultados_treeview.delete(item)
            for producto, modelo, marca, precio, descripcion, stock in datos_productos:
                resultados_treeview.insert("", "end", values=(producto, modelo, marca, precio, descripcion, stock))      


    bm = Toplevel()
    bm.title("Ventana para modificar y dar de baja")
    bm.geometry('600x280')
    bm.config(bg='cyan')

    etiqueta_seleccion = Label(bm, text="Ingrese la marca del Producto que quiera modificar o dar de baja")
    etiqueta_seleccion.grid(row=0, column=0, padx=5, pady=5)
    marca_var.set('')
    seleccion = Entry(bm, textvariable=marca_var)
    seleccion.grid(row=0, column=1, padx=5, pady=5)
    boton_buscar = Button(bm, text="Buscar por Marca", command=buscar_por_marca)
    boton_buscar.grid(row=0, column=2, padx=5, pady=5)

    nuevo_producto_label = Label(bm, text="Nuevo Producto:")
    nuevo_producto_label.grid(row=1, column=0, padx=5, pady=5)
    nuevo_modelo_label = Label(bm, text="Nuevo Modelo:")
    nuevo_modelo_label.grid(row=2, column=0, padx=5, pady=5)
    nuevo_precio_label = Label(bm, text="Nuevo Precio:")
    nuevo_precio_label.grid(row=3, column=0, padx=5, pady=5)
    nuevo_descripcion_label = Label(bm, text="Nueva Descripción:")
    nuevo_descripcion_label.grid(row=4, column=0, padx=5, pady=5)
    nuevo_stock_label = Label(bm, text="Nuevo Stock:")
    nuevo_stock_label.grid(row=5, column=0, padx=5, pady=5)
    
    nuevo_producto_entry = Entry(bm, textvariable=producto_a_modificar)
    nuevo_producto_entry.grid(row=1, column=1, padx=5, pady=5)
    nuevo_modelo_entry = Entry(bm, textvariable=modelo_a_modificar)
    nuevo_modelo_entry.grid(row=2, column=1, padx=5, pady=5)
    nuevo_precio_entry = Entry(bm, textvariable=precio_a_modificar)
    nuevo_precio_entry.grid(row=3, column=1, padx=5, pady=5)
    nuevo_descripcion_entry = Entry(bm, textvariable=descripcion_a_modificar)
    nuevo_descripcion_entry.grid(row=4, column=1, padx=5, pady=5)
    nuevo_stock_entry = Entry(bm, textvariable=stock_a_modificar)
    nuevo_stock_entry.grid(row=5, column=1, padx=5, pady=5)

    boton_modificar = Button(bm, text="Modificar", command=modificar)
    boton_modificar.grid(row=6, column=0, padx=5, pady=10)

    boton_baja = Button(bm, text="Dar de Baja", command=dar_de_baja)
    boton_baja.grid(row=6, column=1, padx=5, pady=10)



   

def carga_datos():
    global tabla, datos_productos, id_producto
    carga_datos = Toplevel()
    carga_datos.title("Ventana de Carga de Datos")
    carga_datos.geometry('850x400')
    carga_datos.config(bg='turquoise1')

    # Variables
    producto = StringVar()
    modelo = StringVar()
    marca = StringVar()
    precio = DoubleVar()
    descripcion = StringVar()
    stock =  StringVar()
    

    producto_label = Label(carga_datos, text="Producto:")
    producto_label.grid(row=0, column=0, padx=5, pady=5)
    producto_entry = Entry(carga_datos, textvariable=producto)
    producto_entry.grid(row=0, column=1, padx=5, pady=5)

    modelo_label = Label(carga_datos, text="Modelo:")
    modelo_label.grid(row=1, column=0, padx=5, pady=5)
    modelo_entry = Entry(carga_datos, textvariable=modelo)
    modelo_entry.grid(row=1, column=1, padx=5, pady=5)

    marca_label = Label(carga_datos, text="Marca:")
    marca_label.grid(row=2, column=0, padx=5, pady=5)
    marca_entry = Entry(carga_datos, textvariable=marca)
    marca_entry.grid(row=2, column=1, padx=5, pady=5)

    Precio_label = Label(carga_datos, text="Precio:")
    Precio_label.grid(row=3, column=0, padx=5, pady=5)
    Precio_entry = Entry(carga_datos, textvariable=precio)
    Precio_entry.grid(row=3, column=1, padx=5, pady=5)
    
    descripcion_label = Label(carga_datos, text="Descripcion:")
    descripcion_label.grid(row=4, column=0, padx=5, pady=5)
    descripcion_entry = Entry(carga_datos, textvariable=descripcion)
    descripcion_entry.grid(row=4, column=1, padx=5, pady=5)
    
    stock_label = Label(carga_datos, text="Stock:")
    stock_label.grid(row=1, column=2, padx=5, pady=5)
    stock_entry = Entry(carga_datos, textvariable=stock)
    stock_entry.grid(row=1, column=3, padx=5, pady=5)

    tabla = ttk.Treeview(carga_datos, columns=( "Producto", "Modelo", "Marca", "Precio", "Descripción", "Stock"))
    tabla.grid(row=5, column=0, columnspan=4)


    
    tabla.column("#0", width=0, stretch=NO)
    tabla.heading("Producto", text="Producto", anchor=CENTER)
    tabla.heading("Modelo", text="Modelo", anchor=CENTER)
    tabla.heading("Marca", text="Marca", anchor=CENTER)
    tabla.heading("Precio", text="Precio", anchor=CENTER)
    tabla.heading("Descripción", text="Descripción", anchor=CENTER)
    tabla.heading("Stock", text="Stock", anchor=CENTER)
    tabla.column("Producto", width=150)
    tabla.column("Modelo", width=150)
    tabla.column("Marca", width=100)
    tabla.column("Precio", width=100)
    tabla.column("Descripción", width=200)
    tabla.column("Stock", width=100)
    
    def agregar():
        producto_valor = producto.get()
        modelo_valor = modelo.get()
        marca_valor = marca.get()
        precio_valor = precio.get()
        descripcion_valor = descripcion.get()
        stock_valor = stock.get()
        

        if producto_valor and modelo_valor and marca_valor and precio_valor and descripcion_valor and stock_valor :
            try:
                cursor = db.cursor()
                cursor.execute("INSERT INTO productos ( producto, modelo, marca,precio,descripcion,stock) VALUES (%s, %s, %s, %s,%s,%s)",
                               ( producto_valor, modelo_valor,marca_valor, precio_valor,descripcion_valor,stock_valor))
                db.commit()
                tabla.insert("", "end", values=( producto_valor, modelo_valor,marca_valor, precio_valor,descripcion_valor,stock_valor))
                datos_productos.append(( producto_valor, modelo_valor,marca_valor, precio_valor,descripcion_valor,stock_valor))
                producto.set("")
                modelo.set("")
                marca.set("")
                precio.set("")
                descripcion.set("")
                stock.set("")
                
                messagebox.showinfo("Éxito", "Los datos se han insertado en la base de datos.")
            except Exception as e:
                db.rollback()
                messagebox.showerror("Error", f"Error al insertar datos en la base de datos: {str(e)}")

    boton_agregar = Button(carga_datos, text="Agregar", command=agregar)
    boton_agregar.grid(row=4,column=2 , padx=5, pady=10)

    db = conectar_bd()
    if db is None:
        messagebox.showerror("Error", "No se pudo conectar a la base de datos.")
    else:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM productos")
        datos_db = cursor.fetchall()
        for row in datos_db:
            datos_productos.append(row)
            tabla.insert("", "end", values=row)
            
def ventana_clientes():
    ventana_clientes=Toplevel(ventana)
    ventana_clientes.geometry("600x400")
    ventana_clientes.config(bg="SeaGreen3")
    ventana_clientes.title("Ventana Principal Clientes")
    cargarc = Button(ventana_clientes, text='Cargar Producto',font=10,height=2, command=cliente)
    cargarc.place(x=100,y=350)
    bmc = Button(ventana_clientes, text='Baja y Modificación de Cliente',font=10,height=2, command=cliente_bm)
    bmc.place(x=250,y=350)
    #fotos = PhotoImage(file='cliente.png')
    imagen_etiqueta_cl = Label(ventana_clientes,image=fotos6)
    imagen_etiqueta_cl.place(x=200, y=80)
    
            
def cliente():
    global tabla2, datos_clientes, dni,seleccion_id
    cliente= Toplevel()
    cliente.geometry("860x470")
    cliente.config(bg='SeaGreen1')
    
    
    dni = StringVar()
    nombre = StringVar()
    apellido = StringVar()
    email = StringVar()
    direccion = StringVar()
    telefono= StringVar()

    dni_label = Label(cliente, text="Dni:")
    dni_label.grid(row=0, column=0, padx=5, pady=5)
    dni_entry = Entry(cliente, textvariable=dni)
    dni_entry.grid(row=0, column=1, padx=5, pady=5)

    nombre_label = Label(cliente, text="Nombre:")
    nombre_label.grid(row=1, column=0, padx=5, pady=5)
    nombre_entry = Entry(cliente, textvariable=nombre)
    nombre_entry.grid(row=1, column=1, padx=5, pady=5)

    apellido_label = Label(cliente, text="Apellido:")
    apellido_label.grid(row=2, column=0, padx=5, pady=5)
    apellido_entry = Entry(cliente, textvariable=apellido)
    apellido_entry.grid(row=2, column=1, padx=5, pady=5)

    email_label = Label(cliente, text="Email:")
    email_label.grid(row=3, column=0, padx=5, pady=5)
    email_entry = Entry(cliente, textvariable=email)
    email_entry.grid(row=3, column=1, padx=5, pady=5)
    
    direccion_label = Label(cliente, text="Direccion:")
    direccion_label.grid(row=4, column=0, padx=5, pady=5)
    direccion_entry = Entry(cliente, textvariable=direccion)
    direccion_entry.grid(row=4, column=1, padx=5, pady=5)
    
    telefono_label = Label(cliente, text="Telefono:")
    telefono_label.grid(row=5, column=0, padx=5, pady=5)
    telefono_entry = Entry(cliente, textvariable=telefono)
    telefono_entry.grid(row=5, column=1, padx=5, pady=5)

    tabla2 = ttk.Treeview(cliente, columns=( "Dni", "Nombre", "Apellido", "Email", "Direccion", "Telefono"))
    tabla2.grid(row=6, column=0, columnspan=4)
    tabla2.column("#0", width=0, stretch=NO)
    tabla2.heading("Dni", text="Dni", anchor=CENTER)
    tabla2.heading("Nombre", text="Nombre", anchor=CENTER)
    tabla2.heading("Apellido", text="Apellido", anchor=CENTER)
    tabla2.heading("Email", text="Email", anchor=CENTER)
    tabla2.heading("Direccion", text="Dirección", anchor=CENTER)
    tabla2.heading("Telefono", text="Telefono", anchor=CENTER)
    
    tabla2.column("Dni", width=150)
    tabla2.column("Nombre", width=150)
    tabla2.column("Apellido", width=100)
    tabla2.column("Email", width=100)
    tabla2.column("Direccion", width=200)
    tabla2.column("Telefono", width=100)
        
    def agregar_cl():
        dni_valor = dni.get()
        nombre_valor = nombre.get()
        apellido_valor = apellido.get()
        email_valor = email.get()
        direccion_valor = direccion.get()
        telefono_valor = telefono.get()
        

        if dni_valor and nombre_valor and apellido_valor and email_valor and direccion_valor and telefono_valor :
            try:
                cursor = db.cursor()
                cursor.execute("INSERT INTO cliente ( dni, nombre, apellido,email,direccion,telefono) VALUES (%s, %s, %s, %s,%s,%s)",
                               ( dni_valor, nombre_valor,apellido_valor, email_valor,direccion_valor,telefono_valor))
                db.commit()
                tabla2.insert("", "end", values=( dni_valor, nombre_valor,apellido_valor, email_valor,direccion_valor,telefono_valor))
                datos_clientes.append(( dni_valor, nombre_valor,apellido_valor, email_valor,direccion_valor,telefono_valor))
                dni.set("")
                nombre.set("")
                apellido.set("")
                email.set("")
                direccion.set("")
                telefono.set("")
                
                messagebox.showinfo("Éxito", "Los datos se han insertado en la base de datos.")
            except Exception as e:
                db.rollback()
                messagebox.showerror("Error", f"Error al insertar datos en la base de datos: {str(e)}")

    boton_agregar_cl = Button(cliente, text="Agregar", command=agregar_cl)
    boton_agregar_cl.grid(row=4,column=2 , padx=5, pady=10)

    db = conectar_bd()
    if db is None:
        messagebox.showerror("Error", "No se pudo conectar a la base de datos.")

        
    else:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM cliente")
        datos_db = cursor.fetchall()
        for row in datos_db:
            datos_clientes.append(row)
            tabla2.insert("", "end", values=row)

    

def cliente_bm():
    global tabla2
    global seleccion_id
    seleccion_id = StringVar()
    cliente_bm = Toplevel()
    cliente_bm.geometry("580x180")
    cliente_bm.config(bg='red')
    email_a_modificar = StringVar()
    direccion_a_modificar = StringVar()
    telefono_a_modificar = StringVar()

    email_label = Label(cliente_bm, text="Nuevo Email:")
    email_label.grid(row=4, column=0, padx=5, pady=5)
    direccion_label = Label(cliente_bm, text="Nueva Dirección:")
    direccion_label.grid(row=5, column=0, padx=5, pady=5)
    telefono_label = Label(cliente_bm, text="Nuevo Teléfono:")
    telefono_label.grid(row=6, column=0, padx=5, pady=5)
    email_entry = Entry(cliente_bm, textvariable=email_a_modificar)
    email_entry.grid(row=4, column=1, padx=5, pady=5)
    direccion_entry = Entry(cliente_bm, textvariable=direccion_a_modificar)
    direccion_entry.grid(row=5, column=1, padx=5, pady=5)
    telefono_entry = Entry(cliente_bm, textvariable=telefono_a_modificar)
    telefono_entry.grid(row=6, column=1, padx=5, pady=5)
    etiqueta_seleccion = Label(cliente_bm, text="Ingrese el Dni del Cliente que quiera modificar o dar de baja")
    etiqueta_seleccion.grid(row=0, column=0, padx=5, pady=5)
    dni_a_buscar_var = StringVar()
    seleccion = Entry(cliente_bm, textvariable=dni_a_buscar_var)
    seleccion.grid(row=0, column=1, padx=5, pady=5)

    def buscar_por_dni_modificar():
        dni_buscar = dni_a_buscar_var.get().strip()  
        if dni_buscar:
            db = conectar_bd()
            cursor = db.cursor()
            cursor.execute("SELECT * FROM cliente WHERE dni = %s", (dni_buscar,))
            cliente_encontrado = cursor.fetchone()
            db.close()
            if cliente_encontrado:
                seleccion_id.set(dni_buscar)   
                email_a_modificar.set(cliente_encontrado[3])
                direccion_a_modificar.set(cliente_encontrado[4])
                telefono_a_modificar.set(cliente_encontrado[5])
                messagebox.showinfo("Resultado de búsqueda", f"Dni: {cliente_encontrado[2]}\nNombre: {cliente_encontrado[0]}\nApellido: {cliente_encontrado[1]}\nEmail: {cliente_encontrado[3]}\nDireccion: {cliente_encontrado[4]}\nTelefono: {cliente_encontrado[5]}")
            else:
                seleccion_id.set("")  
                messagebox.showinfo("Resultado", "No se encontró ningún cliente con ese DNI.")

    boton_buscar_dni = Button(cliente_bm, text="Buscar por DNI", command=buscar_por_dni_modificar)
    boton_buscar_dni.grid(row=0, column=3, padx=5, pady=5)

    def modificar_cl():
        global datos_clientes
        global tabla2
        dni_a_modificar = seleccion_id.get()
        email_a_modificar_valor = email_a_modificar.get()
        direccion_a_modificar_valor = direccion_a_modificar.get()
        telefono_a_modificar_valor = telefono_a_modificar.get()
        if dni_a_modificar:
            db = conectar_bd()
            cursor = db.cursor()
            cursor.execute("UPDATE cliente SET email = %s, direccion = %s, telefono = %s WHERE dni = %s",
                           (email_a_modificar_valor, direccion_a_modificar_valor, telefono_a_modificar_valor, dni_a_modificar))
            db.commit()
            db.close()
            for i, (dni, nombre, apellido, email, direccion, telefono) in enumerate(datos_clientes):
                if dni == dni_a_modificar:
                    datos_clientes[i] = (dni, nombre, apellido, email_a_modificar_valor, direccion_a_modificar_valor, telefono_a_modificar_valor)
                    break
            actualizar_grilla_clientes()
            messagebox.showinfo("Modificación exitosa", "Los datos del cliente fueron modificados con éxito.")

    boton_modificar = Button(cliente_bm, text="Modificar", command=modificar_cl)
    boton_modificar.grid(row=7, column=0, padx=5, pady=10)

    def dar_de_baja_cl():
        global datos_clientes
        global tabla2
        dni_a_dar_de_baja = seleccion_id.get()
        if dni_a_dar_de_baja:
            db = conectar_bd()
            cursor = db.cursor()
            cursor.execute("DELETE FROM cliente WHERE dni = %s", (dni_a_dar_de_baja,))
            db.commit()
            db.close()
            for i, (dni, nombre, apellido, email, direccion, telefono) in enumerate(datos_clientes):
                if dni == dni_a_dar_de_baja:
                    datos_clientes.pop(i)
                    break
            actualizar_grilla_clientes()
            messagebox.showinfo("Dado de baja hecho", "El cliente fue dado de baja con éxito.")

    boton_baja = Button(cliente_bm, text="Dar de Baja", command=dar_de_baja_cl)
    boton_baja.grid(row=7,column=1,padx=5,pady=10)

    def actualizar_grilla_clientes():
        global tabla2
    if tabla2:
        for item in tabla2.get_children():
            tabla2.delete(item)
        for dni, nombre, apellido, email, direccion, telefono in datos_clientes:
            tabla2.insert("", "end", values=(dni, nombre, apellido, email, direccion, telefono))




def ventana_facturas():
    ventana_facturas=Toplevel(ventana)
    ventana_facturas.geometry("600x400")
    ventana_facturas.title("Ventana Principal Facturas")
    ventana_facturas.config(bg="DeepSkyBlue3")
    cargarf = Button(ventana_facturas, text='Generar Factura',font=10,height=2, command=facturas)
    cargarf.place(x=250,y=350)
    imagen_etiqueta_fc = Label(ventana_facturas,image=fotos8)
    imagen_etiqueta_fc.place(x=125, y=0)    
def facturas():
    facturas = Toplevel()
    facturas.geometry("400x400")
    facturas.config(bg="Skyblue")
    facturas.title("Facturas")

    
    nro_factura = StringVar()
    fecha = StringVar()
    cantidad = StringVar()
    precio_total = StringVar()
    id_producto = StringVar()  
    dni = StringVar()  
    nro_factura_label = Label(facturas, text="Numero de Factura:")
    nro_factura_label.place(x=50, y=50)
    nro_factura_entry = Entry(facturas, textvariable=nro_factura)
    nro_factura_entry.place(x=200, y=50)

    fecha_label = Label(facturas, text="Fecha:")
    fecha_label.place(x=50, y=100)
    fecha_entry = Entry(facturas, textvariable=fecha)
    fecha_entry.place(x=200, y=100)

    cantidad_label = Label(facturas, text="Cantidad:")
    cantidad_label.place(x=50, y=150)
    cantidad_entry = Entry(facturas, textvariable=cantidad)
    cantidad_entry.place(x=200, y=150)

    precio_total_label = Label(facturas, text="Precio Total:")
    precio_total_label.place(x=50, y=200)
    precio_total_entry = Entry(facturas, textvariable=precio_total)
    precio_total_entry.place(x=200, y=200)

    id_producto_label = Label(facturas, text="ID del Producto:")
    id_producto_label.place(x=50, y=250)
    id_producto_entry = Entry(facturas, textvariable=id_producto)
    id_producto_entry.place(x=200, y=250)

    dni_label = Label(facturas, text="DNI del Cliente:")
    dni_label.place(x=50, y=300)
    dni_entry = Entry(facturas, textvariable=dni)
    dni_entry.place(x=200, y=300)

    def buscar_cliente_por_dni(dni):
        try:
            db = mysql.connector.connect(
                host="127.0.0.1",
                user="root",
                password="",
                database="tecnologias"
            )

            cursor = db.cursor()
            consulta = "SELECT nombre, apellido FROM cliente WHERE dni = %s"
            cursor.execute(consulta, (dni,))
            cliente = cursor.fetchone()
            cursor.close()
            db.close()
            if cliente:
                return f"{cliente[0]} {cliente[1]}"
            else:
                return None
        except Exception as e:
            print(f"Error al buscar el cliente: {str(e)}")
            return None

    def buscar_producto_por_id(id_producto):
        try:
            db = mysql.connector.connect(
                host="127.0.0.1",
                user="root",
                password="",
                database="tecnologias"
            )

            cursor = db.cursor()
            consulta = "SELECT producto, precio FROM productos WHERE id_producto = %s"
            cursor.execute(consulta, (id_producto,))
            producto = cursor.fetchone()
            cursor.close()
            db.close()
            if producto:
                return producto[0], producto[1]
            else:
                return None, None
        except Exception as e:
            print(f"Error al buscar el producto: {str(e)}")
            return None, None

    def generar_factura():
        nro_factura_valor = nro_factura.get()
        fecha_valor = fecha.get()
        cantidad_valor = cantidad.get()
        precio_total_valor = precio_total.get()
        id_producto_valor = id_producto.get()
        dni_valor = dni.get()

        if nro_factura_valor and fecha_valor and cantidad_valor and precio_total_valor and id_producto_valor and dni_valor:
            try:
                nombre_cliente = buscar_cliente_por_dni(dni_valor)
                nombre_producto, precio_producto = buscar_producto_por_id(id_producto_valor)

                if nombre_cliente and nombre_producto:
                    factura_text = f"Factura N° {nro_factura_valor}\n\n"
                    factura_text += f"Fecha: {fecha_valor}\n\n"
                    factura_text += f"Nombre del Cliente: {nombre_cliente}\n"
                    factura_text += f"Producto: {nombre_producto}\n"
                    factura_text += f"Cantidad: {cantidad_valor}\n"
                    factura_text += f"Precio Total: ${precio_total_valor}\n"

                    factura_ven = Toplevel()
                    factura_ven.geometry("200x200")
                    factura_ven.title(f"Factura N° {nro_factura_valor}")

                    factura_label = Label(factura_ven, text="Factura", font=("Helvetica", 16, "bold"))
                    factura_label.pack()

                    detalle_label = Label(factura_ven, text=factura_text)
                    detalle_label.pack()
                else:
                    messagebox.showerror("Error", "Cliente o producto no encontrados.")
            except Exception as e:
                messagebox.showerror("Error", f"Error al generar la factura: {str(e)}")
                facturas()

    generar_factura_button = Button(facturas, text="Generar Factura", command=generar_factura)
    generar_factura_button.place(x=200, y=350)


        
def salir():
    ventana.destroy()


ventana = Tk()
ventana.title("Local de Tecnología")
ventana.geometry('900x600')
ventana.config(bg='steel blue')
fotos6 = PhotoImage(file='cliente.png').subsample(1)
fotos7 = PhotoImage(file='productos.png').subsample(2)
fotos8 = PhotoImage(file='factura.png').subsample(1)


titulo = Label(ventana, text="BIENVENIDO A NUESTRO LOCAL DE TECNOLOGÍA", font=("Helvetica", 20, "bold"))
titulo.place(x=100, y=10)

foto = PhotoImage(file='Technology-PNG.png').subsample(2)
imagen_etiqueta = Label(ventana, image=foto)
imagen_etiqueta.place(x=200, y=150)

clc = Button(ventana, text='DATOS CLIENTES',font=10,width=20,height=2, command=ventana_clientes)
clc.place(x=100, y=85)

prd = Button(ventana, text='DATOS PRODUCTOS',font=10,width=20,height=2, command=ventana_productos)
prd.place(x=300, y=85)

fc = Button(ventana, text='DATOS FACTURAS',font=10,width=20,height=2, command=ventana_facturas)
fc.place(x=500, y=85)

salir = Button(ventana, text='SALIR',font=10,width=20,height=2,command=salir)
salir.place(x=700, y=85)

ventana.mainloop()

   


