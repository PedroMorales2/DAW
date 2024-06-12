from database.bd_goldenstore import obtener_conexion

def insertar_producto( nombre, descripcion, precio,stock, id_Categoria, ruta_imagen_db, talla, genero):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor: #La fecha_creacion --> se inserta automáticamente
        cursor.execute("INSERT INTO productos(nombre, descripcion, precio, stock,categoria_id, imagen, talla, genero ) VALUES (%s,%s,%s, %s, %s, %s, %s, %s)",
                       (nombre, descripcion, precio, stock, id_Categoria, ruta_imagen_db, talla, genero))
    conexion.commit()
    conexion.close()

def obtener_nombre_categoria():
    conexion = obtener_conexion()
    tipos_documento = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT id, nombre FROM categorias")
        tipos_documento = cursor.fetchall()
    conexion.close()
    return tipos_documento


def obtener_producto():
    conexion = obtener_conexion()
    usuarios = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT id, nombre, descripcion, precio, stock,categoria_id, imagen, fecha_creacion, talla,genero  FROM productos")
        usuarios = cursor.fetchall()
    conexion.close()
    return usuarios

def eliminar_producto(id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("DELETE FROM productos WHERE id = %s", (id,))
    conexion.commit()
    conexion.close()

def obtener_producto_por_id(id):
    conexion = obtener_conexion()
    juego = None
    with conexion.cursor() as cursor:
        cursor.execute(
            "SELECT id, nombre, descripcion, precio, stock,categoria_id, imagen, fecha_creacion, talla  FROM productos WHERE id = %s", (id,))
        juego = cursor.fetchone()
    conexion.close()
    print(juego)
    return juego

def actualizar_producto( nombre, descripcion, precio,stock, id_Categoria, imagen, talla, id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("UPDATE productos SET nombre = %s, descripcion = %s, precio = %s, stock = %s,categoria_id = %s, imagen = %s, talla = %s WHERE id = %s",
                       ( nombre, descripcion,precio,stock, id_Categoria, imagen, talla, id))
    conexion.commit()
    conexion.close()

# Función para obtener todos los productos y enviarlos a la plantilla hombre.html
def obtener_productos():
    conexion = obtener_conexion()
    productos = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT id, nombre, descripcion, precio, stock,categoria_id, imagen, fecha_creacion, talla FROM productos")
        productos = cursor.fetchall()
    conexion.close()
    print(productos)
    return productos

def obtener_productosHombre():
    conexion = obtener_conexion()
    productos = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT id, nombre, descripcion, precio, stock,categoria_id, imagen, fecha_creacion, talla, genero FROM productos WHERE genero = 'Masculino' AND stock > 0")
        productos = cursor.fetchall()
    conexion.close()
    print(productos)
    return productos

def obtener_productosMujer():
    conexion = obtener_conexion()
    productos = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT id, nombre, descripcion, precio, stock,categoria_id, imagen, fecha_creacion, talla, genero FROM productos WHERE genero = 'Femenino' AND stock > 0")
        productos = cursor.fetchall()
    conexion.close()
    print(productos)
    return productos


# Función para obtener un producto por su id
def obtener_producto_por_id(id):
    conexion = obtener_conexion()
    producto = None
    with conexion.cursor() as cursor:
        cursor.execute("SELECT id,nombre, descripcion, precio, stock,categoria_id, imagen, fecha_creacion, talla FROM productos WHERE id = %s", (id,))
        producto = cursor.fetchone()
    conexion.close()
    return producto

def insertar_nuevo_pedido(user_id):
    conexion = obtener_conexion()
    pedido = None
    with conexion.cursor() as cursor:
        cursor.execute("INSERT INTO pedidos(usuario_id, fecha_pedido, total, estado) VALUES (%s, CURRENT_DATE, 0, 'pendiente')", (user_id,))
        pedido = cursor.lastrowid
    conexion.commit()
    conexion.close()
    return pedido

#transaccion
def guardar_detalle(id_producto, cantidad, id_user):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.callproc('insertar_pedido', (id_producto, cantidad, id_user))
    conexion.commit()
    conexion.close()