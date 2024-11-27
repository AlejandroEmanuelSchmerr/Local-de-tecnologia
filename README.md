
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
