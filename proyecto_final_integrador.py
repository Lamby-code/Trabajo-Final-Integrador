# Importo la librería sqlite3 para manejar la base de datos
import sqlite3
# Importo colorama para ponerle estilo a los prints
from colorama import Fore, Style, init

# Inicializar Colorama
init(autoreset=True)

# Atajos de color
INFO = Fore.CYAN + Style.BRIGHT
MENU = Fore.BLUE + Style.BRIGHT
OK = Fore.GREEN + Style.BRIGHT
ERR = Fore.RED + Style.BRIGHT
TITLE = Fore.MAGENTA + Style.BRIGHT
RESET = Style.RESET_ALL

def conexion():
    """
    Establece y retorna un objeto de conexión a la base de datos SQLite 'inventario.db'.

    Valor de Retorno
    ----------------
    sqlite3.Connection
        Un objeto de conexión a la base de datos SQLite 'inventario.db'.
    """
    return sqlite3.connect("inventario.db")

def crear_tabla():
    """
    Crea la tabla productos dentro de la base de datos inventario.db, 
    si dicha tabla aún no existe. La tabla almacena información de inventario, 
    incluyendo identificador, nombre, descripción, cantidad, precio y categoría.
    """
    with conexion() as con:
        con.execute("""
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            descripcion TEXT,
            cantidad INTEGER NOT NULL,
            precio REAL NOT NULL,
            categoria TEXT
        )
        """)

def solicitar_texto(mensaje, opcional=False):
    """
     Solicita una entrada de texto al usuario, asegurando que el dato ingresado no esté vacío, 
    a menos que se especifique como opcional. La entrada se convierte a minúsculas y se eliminan 
    los espacios en blanco iniciales y finales.

    Parámetros
    ----------
    mensaje: str 
        El texto que se mostrará al usuario para solicitar la entrada.
    opcional: bool
        Si es True, permite que el usuario ingrese una cadena vacía. 
        Si es False (valor por defecto), obliga al usuario a ingresar texto no vacío y repite la solicitud hasta que se cumpla.
     
    Valor de Retorno
    ----------------
    str 
        El texto ingresado por el usuario, en minúsculas y sin espacios en blanco al inicio o al final.         
    """
    while True:
        dato = input(INFO + mensaje + RESET).lower().strip()
        if opcional:
            return dato
        elif dato != "":
            return dato
        else:
            print(ERR + "Error: El campo no puede estar vacío.")

def solicitar_entero(mensaje):
    """
    Solicita una entrada al usuario y la valida para asegurar que sea un número entero no negativo. 
    Repite la solicitud indefinidamente hasta que se ingrese un valor válido.
    
    Parámetros
    ----------
    mensaje : str
        El mensaje que se mostrará al usuario para solicitar la entrada.

    Valor de Retorno
    ----------------
    int
        El valor ingresado por el usuario, convertido a un tipo de dato entero (int) y garantizado como no negativo.   
    """
    while True:
        num = input(INFO + mensaje + RESET).strip()
        if num.isdigit() and int(num) >= 0:
            return int(num)
        else:
            print(ERR + "Error: Debe ingresar un número entero positivo.")

def solicitar_real(mensaje):
    """
    Solicita una entrada al usuario y la valida para asegurar que sea un número real no negativo. 
    Repite la solicitud indefinidamente hasta que se ingrese un valor válido. 
    La validación se realiza utilizando un bloque try...except para manejar entradas que no puedan convertirse a tipo float.

    Parámetros
    ----------
    mensaje : str
        El mensaje que se mostrará al usuario para solicitar la entrada.
    
    Valor de Retorno
    ----------------
    float
        El valor ingresado por el usuario, convertido a un tipo de dato real (float) y garantizado como no negativo.   
    """
    while True:
        num_real = input(INFO + mensaje + RESET).strip()
        try:
            valor = float(num_real)
            if valor >= 0:
                return valor
            else:
                print(ERR + "Error: Debe ingresar un número decimal positivo.")
        except ValueError:
            print(ERR + "Error: Debe ingresar un número decimal válido.")

def visualizar_productos(productos):
    """
    Muestra una lista formateada de productos en la consola. 
    La función itera sobre una colección de tuplas de productos y presenta sus detalles en una sola línea por producto. 
    Si la lista está vacía, imprime un mensaje de notificación.

    Parámetros
    ----------
    productos : list of tuples
        Una lista donde cada elemento es una tupla que representa un registro de producto. 
        Se espera que cada tupla contenga los campos (id, nombre, descripcion, cantidad, precio, categoria) en ese orden, 
        como resultado de una consulta a la base de datos.    
    """
    if productos:
        print(TITLE + "\n══════════════════════════════════════════════")
        print("                LISTA DE PRODUCTOS")
        print("══════════════════════════════════════════════" + RESET)
        for id, nombre, descripcion, cantidad, precio, categoria in productos:
            print(
                f"{MENU}ID:{RESET} {id} | "
                f"{MENU}Nombre:{RESET} {nombre} | "
                f"{MENU}Categoría:{RESET} {categoria} | "
                f"{MENU}Precio:{RESET} ${precio} | "
                f"{MENU}Cantidad:{RESET} {cantidad} | "
                f"{MENU}Descripción:{RESET} {descripcion}"
            )
        print(TITLE + "══════════════════════════════════════════════" + RESET)
    else:
        print(ERR + "No se encontraron productos.")

def verificar_registros():
    """
    Verifica la existencia de registros en la tabla productos de la base de datos. 

    Valor de Retorno
    ----------------
    bool
        True si la tabla productos contiene uno o más registros.
        False si la tabla está vacía o si se produce una excepción sqlite3.Error.    
    """
    # Reviso que la base de datos no este vacía
    try:
        with conexion() as con:
            cursor = con.execute("SELECT * FROM productos")
            productos = cursor.fetchall()
            if not productos:
                print(ERR + "No hay productos registrados.")
                return False
    # Notifico si tira error
    except sqlite3.Error as e:
        print(ERR + f"Error al verificar productos: {e}")
        return False
    return True

def pedir_datos_producto():
    """
    Solicita interactivamente al usuario todos los datos necesarios 
    para registrar o actualizar un producto (nombre, descripción, cantidad, precio y categoría). 
    La función utiliza funciones de utilidad validadoras (solicitar_texto, solicitar_entero, solicitar_real) 
    para asegurar la calidad y el tipo de los datos de entrada, y luego los retorna en una tupla.

    Valor de Retorno
    ----------------
    tuple of (str, str, int, float, str)
        name (str): Nombre del producto (obligatorio, en minúsculas).
        description (str): Descripción del producto (opcional, en minúsculas).
        quantity (int): Cantidad en inventario (entero no negativo).
        price (float): Precio del producto (flotante no negativo).
        category (str): Categoría del producto (opcional, en minúsculas).    
    """
    print(TITLE + "\n--- Ingresar datos del producto ---" + RESET)
    name = solicitar_texto("Ingrese el nombre del producto: ")
    description = solicitar_texto("Ingrese la descripción del producto: ", True)
    quantity = solicitar_entero("Ingrese la cantidad: ")
    price = solicitar_real("Ingrese el precio ($): ")
    category = solicitar_texto("Ingrese la categoría: ", True)
    return name, description, quantity, price, category

 
def id_existe(update_id):
    """
     Verifica si existe un producto con el ID proporcionado en la base de datos.

    Parámetros
    ----------
    update_id : int
        ID del producto a buscar.
    
    Valor de Retorno
    ----------------
    bool
        True si se encuentra un producto con el id especificado.
        False si no se encuentra ningún producto con ese id o si se produce una excepción sqlite3.Error.   
    """
    # Me fijo si existe el id en la base de datos
    try:
        with conexion() as con:
            search_id = con.execute("SELECT * FROM productos WHERE id = ?", (update_id,))
            if search_id.fetchone() is None:
                print(ERR + "No se encontró ningún producto con ese ID.")
                return False
            return True
    # En caso de error aviso
    except sqlite3.Error as e:
        print(ERR + f"Error al buscar el ID: {e}")
        return False



def mostrar_menu():
    """
    Muestra las opciones disponibles del menú principal de la aplicación de gestión de inventario.
    """
    print(MENU + Style.BRIGHT + "\n══════════════════════════════════════════════")
    print("                MENÚ PRINCIPAL")
    print("══════════════════════════════════════════════" + RESET)
    print(f"{MENU}1){RESET} Agregar producto")
    print(f"{MENU}2){RESET} Mostrar productos")
    print(f"{MENU}3){RESET} Actualizar producto")
    print(f"{MENU}4){RESET} Eliminar producto")
    print(f"{MENU}5){RESET} Buscar producto")
    print(f"{MENU}6){RESET} Reporte de productos")
    print(f"{MENU}7){RESET} Salir")

# 1 - Registrar nuevos productos
def agregar_producto(name, description, quantity, price, category):
    """
    Agrega un nuevo producto en la base de datos utilizando los datos proporcionados. 

    Parámetros
    ----------
    name : str 
        El nombre del producto.
    description : str 
        La descripción del producto.    
    quantity : int 
        La cantidad en stock del producto.
    price : float 
        El precio unitario del producto.
    category : str 
        La categoría a la que pertenece el producto.   
    """
    # Intento realizar el registro en la base de datos
    try:
        with conexion() as con:
            con.execute("""
            INSERT INTO productos (nombre, descripcion, cantidad, precio, categoria)
            VALUES (?, ?, ?, ?, ?)
            """, (name, description, quantity, price, category))
        print(OK + "Producto registrado correctamente.")
    # Si hay algún error, informo al usuario
    except sqlite3.Error as e:
        print(ERR + f"Error al registrar el producto: {e}")

# 2 - Visualizar datos de los productos registrados
def consultar_productos():
    """
    Recupera todos los registros de la tabla y luego utiliza la función visualizar_productos() para mostrarlos al usuario.   
    """
    # Realizo la consulta a la base de datos y muestra al usuario los productos
    try:
        with conexion() as con:
            cursor = con.execute("SELECT * FROM productos")
            productos = cursor.fetchall()
            visualizar_productos(productos)
    # En caso de error muestro el detalle del mismo
    except sqlite3.Error as e:
        print(ERR + f"Error al consultar los productos: {e}")

# 3 - Actualizar datos de un producto existente por ID
def actualizar_producto(update_id, name, description, quantity, price, category):
    """
    Actualiza un producto existente en la base de datos utilizando el ID proporcionado y los nuevos datos del producto.

    Parámetros
    ----------
    update_id : int 
        ID del producto que se desea actualizar. 
    name : str 
        Nuevo nombre del producto. 
    description : str 
        Nueva descripción del producto. 
    quantity : int 
        Nueva cantidad disponible del producto. 
    price : float 
        Nuevo precio del producto. 
    category : str 
        Nueva categoría del producto.
    """
    # Realizo la actualización en la base de datos
    try:
        with conexion() as con:
            cursor = con.cursor()
            cursor.execute("""
            UPDATE productos
            SET nombre = ?, descripcion = ?, cantidad = ?, precio = ?, categoria = ?
            WHERE id = ?
            """, (name, description, quantity, price, category, update_id))
            affected_rows = cursor.rowcount
        # Verifico si hubo algún cambio en la base de datos
        if affected_rows > 0:
            print(OK + "Producto actualizado correctamente.")
        else:
            # El UPDATE se ejecutó, pero no coincidió con ninguna fila.
            print(ERR + "No se encontró un producto con ese ID.")
    # Si hay algún error aviso al usuario
    except sqlite3.Error as e:
        print(ERR + f"Error al actualizar el producto: {e}")

# 4 - Eliminar un producto por ID
def eliminar_producto(delete_id):
    """
    Elimina un producto de la base de datos según el ID proporcionado.

    Parámetros
    ----------
    delete_id : int
        ID del producto que se desea eliminar.   
    """
    # Realizo la eliminación en la base de datos
    try:
        with conexion() as con:
            cursor = con.cursor()
            cursor.execute("DELETE FROM productos WHERE id = ?", (delete_id,))
            affected_rows = cursor.rowcount
        # Verifico si hubo algún cambio en la base de datos
        if affected_rows > 0:
            print(OK + f"Producto con ID {delete_id} eliminado correctamente.")
        else:
            # El DELETE se ejecutó, pero no coincidió con ninguna fila.
            print(ERR + "No se encontró un producto con ese ID.")
    # Si hay algún error lo muestro en pantalla
    except sqlite3.Error as e:
        print(ERR + f"Error al eliminar el producto: {e}")

# 5-1 - Buscar producto por ID
def buscar_producto_por_id(search_id):
    """
    Busca un producto en la base de datos utilizando su ID y muestra el resultado mediante visualizar_productos().

    Parámetros
    ----------
    search_id : int
        ID del producto que se desea buscar.
    """
    # Realizo la busqueda en la base de datos y muestro el resultado
    try:
        with conexion() as con:
            cursor = con.execute("""SELECT * FROM productos WHERE id = ?""", (search_id,))
            producto = [cursor.fetchone()]
            if producto[0] is None:
                producto = []
            visualizar_productos(producto)
    # Aviso si hay algún error
    except sqlite3.Error as e:
        print(ERR + f"Error al buscar el producto: {e}")

# 5-2 - Buscar producto por Nombre
def buscar_producto_por_nombre(search_name):
    """
    Busca productos en la base de datos cuyo nombre coincida parcial o totalmente con el valor proporcionado.

    Parámetros
    ----------
    search_name : str
        Texto a buscar dentro del campo 'nombre' de los productos.
    """
    # Realizo la búsqueda en la base de datos y muestro los resultados
    try:
        with conexion() as con:
            cursor = con.execute("SELECT * FROM productos WHERE nombre LIKE ?", (f"%{search_name}%",))
            productos = cursor.fetchall()
            visualizar_productos(productos)
    # Aviso si hay algún error
    except sqlite3.Error as e:
        print(ERR + f"Error al buscar el producto: {e}")

# 6 - Reporte de productos con filtro de cantidad máxima
def reporte_productos(max_quantity):
    """
    Genera un reporte de productos cuya cantidad disponible sea menor o igual al valor especificado.

    Parámetros
    ----------
    max_quantity : int
        Cantidad máxima de stock para filtrar los productos incluidos en el reporte.
    """
    # Realizo la consulta con el filtro y muestro los resultados
    try:
        with conexion() as con:
            cursor = con.execute("SELECT * FROM productos WHERE cantidad <= ?", (max_quantity,))
            productos = cursor.fetchall()
            visualizar_productos(productos)
    # Informo en caso de error
    except sqlite3.Error as e:
        print(ERR + f"Error al generar el reporte: {e}")


# --- Programa principal ---

# Creo la tabla de productos si no existe
crear_tabla()
# Bucle principal del programa
while True:
    mostrar_menu()
    # Solicito la opción al usuario
    option = input(INFO + "\nSeleccione una opción: " + RESET).strip()
    # Verifico que la opción sea válida 
    option_valid = option.isdigit() and 1 <= int(option) <= 7
    # Reviso que la opción sea válida
    if option_valid:
        match int(option):
            # Opción 1 - agregar producto
            case 1:
                # Solicito los datos de entrada
                name, description, quantity, price, category = pedir_datos_producto()
                agregar_producto(name, description, quantity, price, category)
            # Opción 2 - mostrar productos
            case 2:
                if verificar_registros():
                    consultar_productos()
                else:
                    continue
            # Opción 3 - actualizar producto
            case 3:
                # Solicito el ID del producto a actualizar
                update_id = solicitar_entero("Ingrese el número de ID del producto que desea actualizar: ")
                if id_existe(update_id):
                    name, description, quantity, price, category = pedir_datos_producto()
                    actualizar_producto(update_id, name, description, quantity, price, category)
                else:
                    continue
            # Opción 4 - eliminar producto
            case 4:
                if verificar_registros():
                    # Solicito el ID del producto a eliminar
                    delete_id = solicitar_entero("Ingrese el número de ID del producto que desea eliminar: ")
                    eliminar_producto(delete_id)
                else:
                    continue
            # Opción 5 - buscar producto
            case 5:
                if verificar_registros():
                    while True:
                        print(TITLE + "\n--- Opciones de búsqueda ---" + RESET)
                        print(f"{MENU}1){RESET} Buscar por ID")
                        print(f"{MENU}2){RESET} Buscar por Nombre")
                        sub_option = solicitar_entero("Seleccione un opción de búsqueda: ")
                        if sub_option == 1:
                            # Solicito el ID del producto a buscar
                            search_id = solicitar_entero("Ingrese el número de ID del producto que desea buscar: ")
                            buscar_producto_por_id(search_id)
                            break
                        elif sub_option == 2:
                            # Solicito el nombre del producto a buscar
                            search_name = solicitar_texto("Ingrese el nombre del producto que desea buscar: ")
                            buscar_producto_por_nombre(search_name)
                            break
                        else:
                            print(ERR + "Opción inválida. Por favor seleccione 1 o 2.")
                else:
                    continue
            # Opción 6 - reporte de productos
            case 6:
                if verificar_registros():
                    # Solicito el filtro para la busqueda
                    max_quantity = solicitar_entero("Ingrese la cantidad máxima: ")
                    reporte_productos(max_quantity)
                else:
                    continue
            # Opción 7 - salir
            case 7:
                print(OK + "\n¡Hasta la próxima!")
                break
    # Si la opción no es válida, le aviso al usuario
    else:
        print(ERR + "Opción inválida. Ingrese un número del 1 al 7.")