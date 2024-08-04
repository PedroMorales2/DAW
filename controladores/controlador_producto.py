from database.bd_goldenstore import obtener_conexion
from pymysql.cursors import DictCursor
from decimal import Decimal


def insertar_producto( nombre, descripcion, precio,stock, id_Categoria, ruta_imagen_db, talla, genero):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor: #La fecha_creacion --> se inserta automáticamente
        cursor.execute("INSERT INTO productos(nombre, descripcion, precio, stock,categoria_id, imagen, talla, genero ) VALUES (%s,%s,%s, %s, %s, %s, %s, %s)",
                       (nombre, descripcion, precio, stock, id_Categoria, ruta_imagen_db, talla, genero))
        ultimo = cursor.lastrowid
    conexion.commit()
    conexion.close()
    return ultimo

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
        cursor.execute("""
        SELECT pro.id, pro.nombre, pro.descripcion, pro.precio, pro.stock,
        ca.nombre, pro.imagen, pro.fecha_creacion, pro.talla,pro.genero  FROM productos pro
        JOIN categorias ca ON ca.id = pro.categoria_id;
        """)
        usuarios = cursor.fetchall()
    conexion.close()
    return usuarios

def obtener_productox3():
    conexion = obtener_conexion()
    usuarios = []
    with conexion.cursor() as cursor:
        cursor.execute("""
        SELECT pro.id, pro.nombre, pro.descripcion, pro.precio, pro.stock,
        ca.nombre, pro.imagen, pro.fecha_creacion, pro.talla,pro.genero  FROM productos pro
        JOIN categorias ca ON ca.id = pro.categoria_id where pro.stock > 0 limit 4 ;
        """)
        usuarios = cursor.fetchall()
    conexion.close()
    return usuarios

def obtener_productox1():
    conexion = obtener_conexion()
    usuarios = []
    with conexion.cursor() as cursor:
        cursor.execute("""
        SELECT imagen FROM productos LIMIT 4
        """)
        usuarios = cursor.fetchall()
    conexion.close()
    return usuarios

def aleatorio():
    conexion = obtener_conexion()
    usuarios = []
    with conexion.cursor() as cursor:
        cursor.execute("""
        SELECT imagen FROM productos ORDER BY RAND() LIMIT 1
        """)
        usuarios = cursor.fetchall()
    conexion.close()
    return usuarios

#def eliminar_producto(id):
 #   conexion = obtener_conexion()
  #  with conexion.cursor() as cursor:
   #     cursor.execute("DELETE FROM productos WHERE id = %s", (id,))
    #conexion.commit()
    #conexion.close()

def eliminar_producto(id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("DELETE FROM productos WHERE id = %s", (id,))
        filas_afectadas = cursor.rowcount
    conexion.commit()
    conexion.close()
    return filas_afectadas > 0

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

#def actualizar_producto( nombre, descripcion, precio,stock, id_Categoria, imagen, talla, id):
 #   conexion = obtener_conexion()
  #  with conexion.cursor() as cursor:
   #     cursor.execute("UPDATE productos SET nombre = %s, descripcion = %s, precio = %s, stock = %s,categoria_id = %s, imagen = %s, talla = %s WHERE id = %s",
    #                   ( nombre, descripcion,precio,stock, id_Categoria, imagen, talla, id))
    #conexion.commit()
    #conexion.close()

def actualizar_producto(nombre, descripcion, precio, stock, id_Categoria, imagen, talla, id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("UPDATE productos SET nombre = %s, descripcion = %s, precio = %s, stock = %s, categoria_id = %s, imagen = %s, talla = %s WHERE id = %s",
                       (nombre, descripcion, precio, stock, id_Categoria, imagen, talla, id))
        filas_afectadas = cursor.rowcount
    conexion.commit()
    conexion.close()
    return filas_afectadas > 0


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




def guardar_detalle(id_producto, cantidad, id_pedido):
    conexion = obtener_conexion()
    try:
        with conexion.cursor(DictCursor) as cursor:
            cursor.execute("""
                INSERT INTO detalles_pedido (pedido_id, producto_id, cantidad)
                VALUES (%s, %s, %s)
            """, (id_pedido, id_producto, cantidad))

            cursor.execute("""
                SELECT SUM(p.precio * dp.cantidad) AS total_pedido
                FROM detalles_pedido dp
                JOIN productos p ON dp.producto_id = p.id
                WHERE dp.pedido_id = %s
            """, (id_pedido,))
            resultado = cursor.fetchone()
            if resultado and resultado['total_pedido'] is not None:
                factor_igv = Decimal('1.18')
                total_pedido = resultado['total_pedido'] * factor_igv
            else:
                total_pedido = Decimal('0.00')

            cursor.execute("""
                UPDATE pedidos SET total = %s WHERE id = %s
            """, (total_pedido, id_pedido))

            cursor.execute("""
                UPDATE productos SET stock = stock - %s WHERE id = %s
            """, (cantidad, id_producto))

            conexion.commit()
    except Exception as e:
        print("Ocurrió un error al procesar el detalle del pedido:", e)
        conexion.rollback()
    finally:
        conexion.close()



 #####apis

def obtener_nombre_categoriaApi():
    conexion = obtener_conexion()
    tipos_documento = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT id, nombre, descripcion,fecha_creacion FROM categorias")
        tipos_documento = cursor.fetchall()
    conexion.close()
    return tipos_documento

def obtener_nombre_categoriaApixid(id):
    conexion = obtener_conexion()
    tipos_documento = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT id, nombre, descripcion,fecha_creacion FROM categorias WHERE id = %s", (id,))
        tipos_documento = cursor.fetchall()
    conexion.close()
    return tipos_documento

def insertar_categoria(nombre,descripcion,fecha_creacion):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("INSERT INTO categorias(nombre, descripcion, fecha_creacion) VALUES (%s, %s, %s)", (nombre, descripcion, fecha_creacion))
        ultimo_id = cursor.lastrowid
    conexion.commit()
    conexion.close()
    return ultimo_id

#def actualizar_categoria(nombre,descripcion,fecha_creacion,id):
 #  conexion = obtener_conexion()
  #  with conexion.cursor() as cursor:
  #      cursor.execute("UPDATE categorias SET nombre = %s, descripcion = %s, fecha_creacion = %s WHERE id = %s", (nombre, descripcion, fecha_creacion, id))

   # conexion.commit()
    #conexion.close()
    #return id

def actualizar_categoria(nombre, descripcion, fecha_creacion, id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("UPDATE categorias SET nombre = %s, descripcion = %s, fecha_creacion = %s WHERE id = %s", (nombre, descripcion, fecha_creacion, id))
        filas_afectadas = cursor.rowcount
    conexion.commit()
    conexion.close()
    return filas_afectadas > 0


#def eliminar_categoria(id):
 #   conexion = obtener_conexion()
  #  with conexion.cursor() as cursor:
   #     cursor.execute("DELETE FROM categorias WHERE id = %s", (id,))
#    conexion.commit()
 #  conexion.close()
  #  return id


def eliminar_categoria(id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("DELETE FROM categorias WHERE id = %s", (id,))
        filas_afectadas = cursor.rowcount
    conexion.commit()
    conexion.close()
    return filas_afectadas > 0