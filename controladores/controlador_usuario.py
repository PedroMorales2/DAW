from database.bd_goldenstore import obtener_conexion
import hashlib

def encriptar_contraseña(contraseña):
    sha256 = hashlib.sha256()
    sha256.update(contraseña.encode('utf-8'))
    return sha256.hexdigest()

def insertar_usuario(nombre, email, telefono, apellido, nombre_usuario, contrasenia, fecha_nacimiento, tipo_Usuario):
    contrasenia_hash = encriptar_contraseña(contrasenia)
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("INSERT INTO usuarios(nombre, email, telefono, apellido, nombredeusuario, contraseña, fechaNacimiento, tipo_usuario_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                       (nombre, email, telefono, apellido, nombre_usuario, contrasenia_hash, fecha_nacimiento, tipo_Usuario))
        conexion.commit()
        ultimo = cursor.lastrowid
    conexion.close()
    return ultimo

def actualizar_token_usuario(usuario, token):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("UPDATE usuarios SET token =%s WHERE email = %s ",
                       (token, usuario))
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


#def eliminar_usuario(id):
    #conexion = obtener_conexion()
    #with conexion.cursor() as cursor:
     #   cursor.execute("DELETE FROM usuarios WHERE id = %s", (id,))
    #conexion.commit()
    #conexion.close()

def eliminar_usuario(id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("DELETE FROM usuarios WHERE id = %s", (id,))
        filas_afectadas = cursor.rowcount
    conexion.commit()
    conexion.close()
    return filas_afectadas > 0


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
    contrasenia_hash = encriptar_contraseña(contrasenia)
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("UPDATE usuarios SET nombre= %s, email = %s, telefono= %s, apellido= %s, nombredeusuario= %s,contraseña= %s,fechaNacimiento= %s, tipo_usuario_id = %s WHERE id = %s",
                       (nombre, email, telefono, apellido,nombre_usuario,contrasenia_hash,fecha_nacimiento,tipo_Usuario, id))
    conexion.commit()
    conexion.close()

#nombre,apellido,email,telefono,contraseña,fechaNacimiento
def actualizar_usuarioXuser(nombre, apellido, email,telefono,contrasenia,fecha_nacimiento, id):
    contrasenia_hash = encriptar_contraseña(contrasenia)
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("UPDATE usuarios SET nombre= %s, apellido = %s, email= %s, telefono= %s, contraseña= %s,fechaNacimiento=%s WHERE id = %s",
                       (nombre, apellido, email,telefono,contrasenia_hash,fecha_nacimiento, id))
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
    contrasenia_hash = encriptar_contraseña(contrasenia)
    conexion = obtener_conexion()
    usuarios = []
    try:
        with conexion.cursor() as cursor:
            cursor.execute("SELECT tipo_usuario_id, id, nombre, token, email FROM usuarios WHERE email = %s AND contraseña = %s", (usuario, contrasenia_hash))
            usuarios = cursor.fetchall()
    except Exception as e:
        print(f"Error durante el login: {e}")
    finally:
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
        ultimo = cursor.lastrowid
    conexion.commit()
    conexion.close()
    return ultimo


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


def obtener_usuario_por_id_auth(id):
    conexion = obtener_conexion()
    usuario = None
    try:
        with conexion.cursor() as cursor:
            cursor.execute(
                "SELECT id, nombredeusuario, contraseña FROM usuarios WHERE id = %s", (id,))
            usuario = cursor.fetchone()
    except Exception as e:
        print(f"Error durante la consulta: {e}")
    finally:
        conexion.close()
    return usuario



def obtener_user_por_username(username):
    conexion = obtener_conexion()
    usuario = None
    try:
        with conexion.cursor() as cursor:
            print(f"Buscando usuario con nombredeusuario: {username}")
            cursor.execute(
                "SELECT id, nombredeusuario, contraseña FROM usuarios WHERE nombredeusuario = %s", (username,))
            usuario = cursor.fetchone()
            print(f"Resultado de la consulta: {usuario}")
    except Exception as e:
        print(f"Error durante la consulta: {e}")
    finally:
        conexion.close()
    return usuario





###apis pedro


def obtener_nombre_tipo_usuario_x_id(id):
    conexion = obtener_conexion()
    tipos_usuario = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT id, nombre  FROM tipo_usuario WHERE id = %s", (id,))
        tipos_usuario = cursor.fetchall()
    conexion.close()
    return tipos_usuario

def insertar_tipo_usuario(nombre):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("INSERT INTO tipo_usuario(nombre) VALUES (%s)",
                       (nombre,))
        ultimo_id = cursor.lastrowid
    conexion.commit()
    conexion.close()
    return ultimo_id

def actualizar_tipo_usuario(nombre, id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("UPDATE tipo_usuario SET nombre = %s WHERE id = %s", (nombre, id))
        filas_afectadas = cursor.rowcount
    conexion.commit()
    conexion.close()
    return filas_afectadas > 0


#def eliminar_tipo_usuario(id):
 #   conexion = obtener_conexion()
  #  with conexion.cursor() as cursor:
   #     cursor.execute("DELETE FROM tipo_usuario WHERE id = %s", (id,))
#    conexion.commit()
 #   conexion.close()

def eliminar_tipo_usuario(id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("DELETE FROM tipo_usuario WHERE id = %s", (id,))
        filas_afectadas = cursor.rowcount
    conexion.commit()
    conexion.close()
    return filas_afectadas > 0


def obtener_tajerta():
    conexion = obtener_conexion()
    tarjetas = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT id, numero_tarjeta, nombre_titular, fecha_expiracion, codigo_seguridad, usuario_id FROM tarjetas")
        tarjetas = cursor.fetchall()
    conexion.close()
    return tarjetas


def api_ver_tarjetas(id):
    conexion = obtener_conexion()
    tarjetas = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT id, numero_tarjeta, nombre_titular, fecha_expiracion, codigo_seguridad, usuario_id FROM tarjetas WHERE id = %s", (id,))
        tarjetas = cursor.fetchall()
    conexion.close()
    return tarjetas

#def actualizar_tarjeta(numero_tarjeta, nombre_titular, fecha_expiracion, codigo_seguridad, usuario_id, id):
    #conexion = obtener_conexion()
    #with conexion.cursor() as cursor:
     #   cursor.execute("UPDATE tarjetas SET numero_tarjeta= %s, nombre_titular = %s, fecha_expiracion= %s, codigo_seguridad= %s, usuario_id= %s WHERE id = %s",
      #                 (numero_tarjeta, nombre_titular, fecha_expiracion, codigo_seguridad, usuario_id, id))
    #conexion.commit()
    #conexion.close()

def actualizar_tarjeta(numero_tarjeta, nombre_titular, fecha_expiracion, codigo_seguridad, usuario_id, id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("UPDATE tarjetas SET numero_tarjeta= %s, nombre_titular = %s, fecha_expiracion= %s, codigo_seguridad= %s, usuario_id= %s WHERE id = %s",
                       (numero_tarjeta, nombre_titular, fecha_expiracion, codigo_seguridad, usuario_id, id))
        filas_afectadas = cursor.rowcount
    conexion.commit()
    conexion.close()
    return filas_afectadas > 0


#def eliminar_tarjeta(id):
 #   conexion = obtener_conexion()
  #  with conexion.cursor() as cursor:
   #     cursor.execute("DELETE FROM tarjetas WHERE id = %s", (id,))
    #conexion.commit()
    #conexion.close()

def eliminar_tarjeta(id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("DELETE FROM tarjetas WHERE id = %s", (id,))
        filas_afectadas = cursor.rowcount
    conexion.commit()
    conexion.close()
    return filas_afectadas > 0


def obtener_direccion():
    conexion = obtener_conexion()
    direcciones = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT id, pais, departamento, ciudad, codigo_postal, direccion1, direccion2, usuarios_id FROM direccion")
        direcciones = cursor.fetchall()
    conexion.close()
    return direcciones

def obtener_direccion_por_id(id):
    conexion = obtener_conexion()
    direcciones = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT id, pais, departamento, ciudad, codigo_postal, direccion1, direccion2, usuarios_id FROM direccion WHERE id = %s", (id,))
        direcciones = cursor.fetchall()
    conexion.close()
    return direcciones

def insertar_direccion(pais, departamento, ciudad, codigo_postal, direccion1, direccion2, usuarios_id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("INSERT INTO direccion(pais, departamento, ciudad, codigo_postal, direccion1, direccion2, usuarios_id) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                       (pais, departamento, ciudad, codigo_postal, direccion1, direccion2, usuarios_id))
        ultimo = cursor.lastrowid
    conexion.commit()
    conexion.close()
    return ultimo


def actualizar_direccion(pais, departamento, ciudad, codigo_postal, direccion1, direccion2, usuarios_id, id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("UPDATE direccion SET pais= %s, departamento = %s, ciudad= %s, codigo_postal= %s, direccion1= %s, direccion2= %s, usuarios_id= %s WHERE id = %s",
                       (pais, departamento, ciudad, codigo_postal, direccion1, direccion2, usuarios_id, id))
    conexion.commit()
    conexion.close()

def eliminar_direccion(id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("DELETE FROM direccion WHERE id = %s", (id,))
    conexion.commit()
    conexion.close()

def api_pago():
    conexion = obtener_conexion()
    pagos = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT id,pedido_id, tarjeta_id,fecha_pago,monto,estado FROM pagos")
        pagos = cursor.fetchall()
    conexion.close()
    return pagos

def api_pago_por_id(id):
    conexion = obtener_conexion()
    pagos = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT id,pedido_id, tarjeta_id,fecha_pago,monto,estado FROM pagos WHERE id = %s", (id,))
        pagos = cursor.fetchall()
    conexion.close()
    return pagos

def insertar_pago_return( pedido_id, tarjeta_id ,total_pago):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.callproc("realizar_pago", (pedido_id, tarjeta_id ,total_pago))
        ultimo = cursor.execute("select count(*) + 1 from pagos")
    conexion.commit()
    conexion.close()
    return ultimo

def actualizar_pago(fecha_pago, total, pedido_id, tarjeta_id, id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("UPDATE pagos SET fecha_pago= %s, monto = %s, pedido_id= %s, tarjeta_id= %s, estado = 'completado' WHERE id = %s",
                       (fecha_pago, total, pedido_id, tarjeta_id, id))
    conexion.commit()
    conexion.close()


def eliminar_pago(id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("DELETE FROM pagos WHERE id = %s", (id,))
    conexion.commit()
    conexion.close()



    #### agregados
def contador_usuarios():
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) as con FROM usuarios")
        result = cursor.fetchone()
        return {'con': result[0]}
    conexion.close()

def contador_productos():
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) as con FROM productos")
        result = cursor.fetchone()
        return {'con': result[0]}
    conexion.close()

def contador_producto_sin_stock():
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) AS con FROM productos p WHERE p.stock <= 0")
        result = cursor.fetchone()
        return {'con': result[0]}
    conexion.close()

def contador_pedidos():
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) as con FROM pedidos")
        result = cursor.fetchone()
        return {'con': result[0]}
    conexion.close()

def contador_pedidos_pendientes():
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) as con FROM pedidos_pendiente")
        result = cursor.fetchone()
        return {'con': result[0]}
    conexion.close()

def contador_pedidos_enviados():
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) as con FROM pedidos_enviados")
        result = cursor.fetchone()
        return {'con': result[0]}
    conexion.close()

def contador_pagos():
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) as con FROM pagos")
        result = cursor.fetchone()
        return {'con': result[0]}
    conexion.close()




#######MANTENIMIENTO

def obtener_mantenimiento_tarjeta():
    conexion = obtener_conexion()
    productos = []
    with conexion.cursor() as cursor:
        cursor.execute("""
                       SELECT tar.id,usu.nombre, tar.numero_tarjeta,tar.nombre_titular,
                            tar.fecha_expiracion, tar.codigo_seguridad
                            FROM tarjetas tar
                            JOIN usuarios usu ON tar.usuario_id = usu.id
                        """)
        productos = cursor.fetchall()
    conexion.close()
    return productos

def obtener_mantenimiento_tarjeta_x_id(id):
    conexion = obtener_conexion()
    productos = []
    with conexion.cursor() as cursor:
        cursor.execute("""
                       SELECT tar.id,usu.nombre, tar.numero_tarjeta,tar.nombre_titular,
                            tar.fecha_expiracion, tar.codigo_seguridad, usu.id
                            FROM tarjetas tar
                            JOIN usuarios usu ON tar.usuario_id = usu.id
                            where tar.id = %s
                        """, (id,) )
        productos = cursor.fetchone()
    conexion.close()
    return productos


def obtener_direccion_MANTENIMIENTO():
    conexion = obtener_conexion()
    direcciones = []
    with conexion.cursor() as cursor:
        cursor.execute("""
                       SELECT usu.nombre,direccion.id, pais, departamento, ciudad, codigo_postal, direccion1, direccion2 FROM direccion
                        JOIN usuarios usu ON direccion.usuarios_id = usu.id
                       """)
        direcciones = cursor.fetchall()
    conexion.close()
    return direcciones

def obtener_direccion_id_MANTENIMIENTO(id):
    conexion = obtener_conexion()
    direcciones = []
    with conexion.cursor() as cursor:
        cursor.execute("""
                       SELECT usu.id,usu.nombre,direccion.id, pais, departamento, ciudad, codigo_postal, direccion1, direccion2 FROM direccion
                        JOIN usuarios usu ON direccion.usuarios_id = usu.id
                        where direccion.id = %s
                       """, (id,))
        direcciones = cursor.fetchone()
    conexion.close()
    return direcciones


def obtener_nombre_tipo_usuario_x_idA(id):
    conexion = obtener_conexion()
    tipos_usuario = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT id, nombre  FROM tipo_usuario WHERE id = %s", (id,))
        tipos_usuario = cursor.fetchone()
    conexion.close()
    return tipos_usuario



def ver_pedidos_general_enviados():
    conexion = obtener_conexion()
    estados = []
    with conexion.cursor() as cursor:
        cursor.execute("SET lc_time_names = 'es_ES';")
        cursor.execute("""
                       SELECT usu.nombre, usu.email ,pe.* FROM pedidos_enviados pe
                        JOIN usuarios usu ON pe.id_usuario = usu.id
                       """)
        estados = cursor.fetchall()
    conexion.close()
    return estados


def ver_pedidos_general_PENDIENTE():
    conexion = obtener_conexion()
    estados = []
    with conexion.cursor() as cursor:
        cursor.execute("SET lc_time_names = 'es_ES';")
        cursor.execute("""
                       SELECT usu.nombre, usu.email,pe.* FROM pedidos_pendiente pe
                        JOIN usuarios usu ON pe.id_usuario = usu.id
                       """)
        estados = cursor.fetchall()
    conexion.close()
    return estados

