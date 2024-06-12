from database.bd_goldenstore import obtener_conexion


def insertar_usuario(nombre, email, telefono, apellido, nombre_usuario,contrasenia,fecha_nacimiento,tipo_Usuario):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("INSERT INTO usuarios(nombre,email,telefono,apellido,nombredeusuario,contraseña,fechaNacimiento,tipo_usuario_id) VALUES (%s,%s, %s, %s, %s, %s, %s, %s)",
                       (nombre, email, telefono, apellido, nombre_usuario,contrasenia,fecha_nacimiento,tipo_Usuario))
    conexion.commit()
    conexion.close()



def obtener_usuarios():
    conexion = obtener_conexion()
    usuarios = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT id, nombre, email, telefono, apellido, nombredeusuario, contraseña, fechaNacimiento, fecha_creacion, tipo_usuario_id  FROM usuarios")
        usuarios = cursor.fetchall()
    conexion.close()
    return usuarios


def eliminar_usuario(id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("DELETE FROM usuarios WHERE id = %s", (id,))
    conexion.commit()
    conexion.close()


def obtener_usuario_por_id(id):
    conexion = obtener_conexion()
    juego = None
    with conexion.cursor() as cursor:
        cursor.execute(
            "SELECT id, nombre, email, telefono, apellido, nombredeusuario, contraseña, fechaNacimiento, tipo_usuario_id  FROM usuarios WHERE id = %s", (id,))
        juego = cursor.fetchone()
    conexion.close()
    return juego

def obtener_pase_por_nombre_de_usuario(username):
    conexion = obtener_conexion()
    usuario = None
    try:
        with conexion.cursor() as cursor:
            print(f"Buscando usuario con nombredeusuario: {username}")
            cursor.execute(
                "SELECT id, nombre, email, telefono, apellido, nombredeusuario, contraseña, fechaNacimiento, tipo_usuario_id FROM usuarios WHERE nombredeusuario = %s", (username,))
            usuario = cursor.fetchone()
            print(f"Resultado de la consulta: {usuario}")
    except Exception as e:
        print(f"Error durante la consulta: {e}")
    finally:
        conexion.close()
    return usuario


#nombre,email,telefono,apellido,nombredeusuario,contraseña,fechaNacimiento,fecha_creacion,tipo_usuario_id
def actualizar_usuario(nombre, email, telefono, apellido, nombre_usuario,contrasenia,fecha_nacimiento,tipo_Usuario, id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("UPDATE usuarios SET nombre= %s, email = %s, telefono= %s, apellido= %s, nombredeusuario= %s,contraseña= %s,fechaNacimiento= %s, tipo_usuario_id = %s WHERE id = %s",
                       (nombre, email, telefono, apellido,nombre_usuario,contrasenia,fecha_nacimiento,tipo_Usuario, id))
    conexion.commit()
    conexion.close()
    
#nombre,apellido,email,telefono,contraseña,fechaNacimiento
def actualizar_usuarioXuser(nombre, apellido, email,telefono,contraseña,fecha_nacimiento, id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("UPDATE usuarios SET nombre= %s, apellido = %s, email= %s, telefono= %s, contraseña= %s,fechaNacimiento=%s WHERE id = %s",
                       (nombre, apellido, email,telefono,contraseña,fecha_nacimiento, id))
    conexion.commit()
    conexion.close()


def obtener_nombre_tipo_usuario():
    conexion = obtener_conexion()
    tipos_usuario = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT id, nombre  FROM tipo_usuario")
        tipos_usuario = cursor.fetchall()
    conexion.close()
    return tipos_usuario

def login(usuario, contrasenia):
    conexion = obtener_conexion()
    usuarios = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT tipo_usuario_id, id, nombre  FROM usuarios where email = %s and contraseña = %s", (usuario, contrasenia))
        usuarios = cursor.fetchall()
    conexion.close()
    return usuarios


def ver_pedidos_pendientes(id):
    conexion = obtener_conexion()
    estados = []
    with conexion.cursor() as cursor:
        cursor.execute("SET lc_time_names = 'es_ES';")
        cursor.execute("SELECT * FROM pedidos_pendiente WHERE id_usuario = %s", (id,))
        estados = cursor.fetchall()
    conexion.close()
    return estados


def ver_tarjetas(id):
    conexion = obtener_conexion()
    tarjetas = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT id, numero_tarjeta, nombre_titular, fecha_expiracion, codigo_seguridad FROM tarjetas WHERE usuario_id = %s", (id,))
        tarjetas = cursor.fetchall()
    conexion.close()
    return tarjetas

def agregar_tarjeta( numero_tarjeta, nombre_titular, fecha_expiracion, codigo_seguridad, usuario_id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("INSERT INTO tarjetas(numero_tarjeta, nombre_titular, fecha_expiracion, codigo_seguridad, usuario_id) VALUES (%s, %s, %s, %s, %s)",
                       (numero_tarjeta, nombre_titular, fecha_expiracion, codigo_seguridad, usuario_id))
    conexion.commit()
    conexion.close()
    
    

def pago_pedido(id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("SELECT pe.id,pe.fecha_pedido, pe.total FROM pedidos pe WHERE pe.id = %s", (id,))
        return cursor.fetchone()
    conexion.close()
    
def detalle_pedido(id):
    conexion = obtener_conexion()
    persona = []
    with conexion.cursor() as cursor:
        cursor.execute("""
                       SELECT pro.nombre, pro.genero ,de.cantidad, de.cantidad * pro.precio AS precio_sub ,pro.imagen FROM detalles_pedido de
                        JOIN productos pro ON de.producto_id = pro.id 
                        WHERE de.pedido_id = %s

                       """, (id,))
        persona = cursor.fetchall()
        return persona
    conexion.close()
    
def insertar_pago( pedido_id, tarjeta_id ,total_pago):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.callproc("realizar_pago", (pedido_id, tarjeta_id ,total_pago))
    conexion.commit()
    conexion.close()
    
def historial_pedido(id):
    conexion = obtener_conexion()
    persona = []
    with conexion.cursor() as cursor:
        cursor.execute("SET lc_time_names = 'es_ES';")
        cursor.execute("""
                       SELECT * FROM pedidos_enviados WHERE id_usuario = %s
                       """, (id,))
        persona = cursor.fetchall()
        return persona
    conexion.close()
    
def historial_detalle_pedido(id):
    conexion = obtener_conexion()
    persona = []
    with conexion.cursor() as cursor:
        cursor.execute("""
                       SELECT pro.imagen,pro.nombre, pro.precio, pro.talla, pro.genero,de.cantidad, pro.precio * de.cantidad as sub_total
                       FROM pedidos pe
                        JOIN detalles_pedido de ON pe.id = de.pedido_id
                        JOIN productos pro ON pro.id = de.producto_id
                        WHERE pe.id = %s
                       """, (id,))
        persona = cursor.fetchall()
        return persona
    conexion.close()