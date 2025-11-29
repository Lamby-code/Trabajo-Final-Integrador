# 📦 Sistema de Gestión de Inventario (SGI) con SQLite y Colorama

## ✨ Descripción del Proyecto

El **Sistema de Gestión de Inventario (SGI)** es una herramienta de consola minimalista y eficiente diseñada para administrar el stock de productos. Permite realizar las operaciones **CRUD** (Crear, Leer, Actualizar, Eliminar) sobre una base de datos local **SQLite**, garantizando la persistencia de los datos en el archivo `inventario.db`.

La interfaz de usuario está mejorada con la librería **Colorama**, lo que proporciona una experiencia de consola clara y visualmente atractiva, diferenciando los mensajes de información, éxito y error mediante el uso de colores. 

---

## 🚀 Características Principales

* **Persistencia de Datos:** Utiliza **SQLite3** para almacenar de forma segura todos los registros.
* **Interfaz Clara:** Implementa **Colorama** para mensajes de consola codificados por colores, mejorando la legibilidad y la experiencia del usuario.
* **Validación Robusta:** Asegura que los datos ingresados (texto, enteros y valores reales/float) sean válidos y no negativos antes de la inserción o actualización.
* **Gestión Completa de Stock:** Soporte para agregar, visualizar, actualizar, eliminar y buscar productos.
* **Búsqueda Flexible:** Permite buscar productos por **ID** exacto o por coincidencia parcial de **Nombre**.
* **Reportes de Stock Mínimo:** Genera un listado de productos con stock bajo (cantidad $\le$ límite definido).

---

## ⚙️ Requisitos del Sistema

Para ejecutar este proyecto, necesitas tener instalado lo siguiente:

* **Python 3.x**
* **PIP (Package Installer for Python)**
* **La librería `colorama`** (gestionada a través de `requirements.txt`).

---

## 📥 Instalación

Dado que ya has creado el archivo `requirements.txt` con la dependencia `colorama`, solo necesitas ejecutar un comando para instalar las librerías necesarias:

```bash
pip install -r requirements.txt
```

La librería `sqlite3` está incluida en la instalación estándar de Python.

---

## ▶️ Cómo Ejecutar el Programa

Ejecuta el script de Python directamente desde tu terminal:

```bash
python app.py
```

*(Asegúrate de reemplazar `app.py` con el nombre real de tu archivo Python.)*

Al iniciar, si no existe, el programa creará automáticamente el archivo de base de datos `inventario.db` y te presentará el menú principal.

---

## 📋 Opciones del Menú Principal

| Opción | Descripción |
|--------|-------------|
| **1** | Agregar producto: Solicita nombre, descripción, cantidad, precio y categoría para un nuevo producto. |
| **2** | Mostrar productos: Lista todos los productos registrados en la base de datos. |
| **3** | Actualizar producto: Permite modificar los datos de un producto existente, identificándolo primero por su ID. |
| **4** | Eliminar producto: Borra un producto de forma permanente, solicitando su ID. |
| **5** | Buscar producto: Ofrece opciones para buscar por ID o por Nombre. |
| **6** | Reporte de productos: Muestra productos cuyo stock (cantidad) es igual o menor a un valor que definas. |
| **7** | Salir: Finaliza la ejecución del programa. |

---

## 📝 Ejemplos de Uso

**Ejemplo 1: Agregar un Producto (Opción 1)**

```text
Seleccione una opción: 1

--- Ingresar datos del producto ---
Ingrese el nombre del producto: Cable HDMI
Ingrese la descripción del producto: 2 metros, 4K
Ingrese la cantidad: 50
Ingrese el precio ($): 12.50
Ingrese la categoría: Accesorios
Producto registrado correctamente.
```

**Ejemplo 2: Actualizar Producto por ID (Opción 3)**

```text
Seleccione una opción: 3
Ingrese el número de ID del producto que desea actualizar: 1

--- Ingresar datos del producto ---
Ingrese el nombre del producto: Cable HDMI Pro
Ingrese la descripción del producto: 3 metros, 8K (Opcional)
Ingrese la cantidad: 45
Ingrese el precio ($): 18.00
Ingrese la categoría: Accesorios Premium
Producto actualizado correctamente.
```

## 📧 Autor

**Proyecto desarrollado por Alan Baez.**