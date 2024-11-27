
# **Proyecto de Local de Tecnología con Tkinter y MySQL**

Este es un proyecto de aplicación de escritorio para la gestión de un local de tecnología, desarrollado en **Python** utilizando **Tkinter** para la interfaz gráfica y **MySQL** para gestionar la base de datos. Este sistema permite gestionar los **clientes**, **productos** y **facturas**.

---

## **Estado del proyecto**  
El proyecto está casi terminado, pero aún faltan algunos ajustes y funcionalidades por implementar.

---

## **Requisitos**

- **Python 3.8 o superior**
- **XAMPP** para ejecutar el servidor MySQL.
- Librerías necesarias para ejecutar el proyecto:
  
  ```bash
  pip install mysql-connector-python
  pip install tk
  ```

---

## **Instalación y Configuración**

### **1. Instalar Python**
- Descarga e instala Python desde [aquí](https://www.python.org/downloads/).
- Asegúrate de marcar la opción "Add Python to PATH" durante la instalación.
- Para verificar que Python se instaló correctamente, abre una terminal o línea de comandos y ejecuta:

  ```bash
  python --version
  ```

### **2. Instalar XAMPP**
- Descarga e instala XAMPP desde [aquí](https://www.apachefriends.org/index.html).
- Abre el panel de control de XAMPP y enciende los servicios de **Apache** y **MySQL**.

### **3. Configurar la Base de Datos**
- Abre **phpMyAdmin** desde XAMPP en `http://localhost/phpmyadmin`.
- Crea una nueva base de datos llamada **tecnologias**.
- Importa el archivo **tecnologias.sql** que se encuentra en este repositorio:
  1. Haz clic en la pestaña **Importar**.
  2. Selecciona el archivo **tecnologias.sql**.
  3. Haz clic en **Continuar** para importar la estructura y los datos de la base de datos.

---

## **Ejecución del Proyecto**

1. Asegúrate de que los servicios de **Apache** y **MySQL** estén activos en XAMPP.
2. Ejecuta el archivo principal del proyecto con el siguiente comando:

   ```bash
   python trabajo_muestra_bd.py
   ```

   Esto abrirá la interfaz gráfica de la aplicación, donde podrás gestionar clientes, productos y facturas desde la base de datos.

---

## **Detalles de la Aplicación**

Al ejecutar el programa, verás una pantalla principal con el mensaje **"Bienvenido a nuestro local de tecnología"** y los siguientes botones:  
- **Datos Clientes**  
- **Datos Productos**  
- **Datos Facturas**  
- **Salir**  

### **1. Gestión de Clientes**
- Al presionar **Datos Clientes**, se abrirá la ventana principal de gestión de clientes con dos opciones:  
  - **Cargar Cliente**:  
    - Muestra un formulario donde se pueden ingresar los datos del cliente.  
    - Después de agregar, los datos se visualizan en un **Treeview** con la lista de todos los clientes registrados.  
  - **Baja y Modificación del Cliente**:  
    - Permite buscar un cliente ingresando su **DNI**.  
    - Filtra y muestra los datos del cliente en el formulario.  
    - Se pueden realizar modificaciones o dar de baja al cliente.

### **2. Gestión de Productos**
- Al presionar **Datos Productos**, se abrirá la ventana principal de gestión de productos con tres opciones:  
  - **Cargar Producto**:  
    - Muestra un formulario para cargar nuevos productos.  
    - Los productos ingresados se listan en una tabla.  
  - **Baja y Modificación del Producto**:  
    - Permite filtrar productos por **marca**.  
    - Los datos del producto pueden ser modificados o eliminados.  
  - **Filtración de Productos**:  
    - Permite buscar y visualizar información específica sobre los productos registrados.

### **3. Gestión de Facturas**
- Al presionar **Datos Facturas**, se abrirá la ventana principal de facturación con las siguientes funcionalidades:  
  - **Generar Factura**:  
    - Muestra un formulario para generar una factura ingresando:  
      - Número de factura  
      - Fecha  
      - Cantidad  
      - Precio total  
      - ID del producto  
      - DNI del cliente  
    - Una vez completado el formulario, se genera la factura y queda registrada en la base de datos.

### **4. Salir**
- El botón **Salir** detiene la ejecución del programa y cierra la aplicación.

---

## **Archivos en este Repositorio**

- **trabajo_muestra_bd.py**: El archivo principal de Python para ejecutar la aplicación.
- **tecnologias.sql**: El archivo SQL para crear y poblar la base de datos.
- **imagenes**: Las imágenes utilizadas en la interfaz gráfica.

---

## **Autor**

**Emanuel Schmer**  
Contacto: emanuelschmer@hotmail.com  

---

¡Gracias por usar este proyecto! 😊  
