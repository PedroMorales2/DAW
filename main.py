from flask import Flask, render_template, request, redirect, flash, jsonify, session, url_for, make_response
from flask_jwt import JWT, jwt_required, current_identity
from functools import wraps
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash
import hashlib
import os
import requests
import random
import logging
import controladores.controlador_producto as controlador_producto
import controladores.controlador_usuario as controlador_usuario
import clases.clase_usuario as clase_usuario
import clases.clase_producto as clase_producto
import clases.clase_categoria as clase_categoria
import clases.clase_tipo_usuario as clase_tipo_usuario
import clases.clase_tajertas as clase_tarjeta
import clases.clase_direccion as clase_direccion
import clases.clase_pago as clase_pago
from hashlib import sha256

class User(object):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def __str__(self):
        return "User(id='%s')" % self.id

def authenticate(username, password):
    userfrombd = controlador_usuario.obtener_user_por_username(username)
    user = None
    if userfrombd is not None:
        user = User(userfrombd[0], userfrombd[1], userfrombd[2])
    if user is not None:
        hashed_password = sha256(password.encode('utf-8')).hexdigest()
        if (user.password == password) or (user.password == hashed_password):
            return user
    return None

def identity(payload):
    user_id = payload['identity']
    userfrombd = controlador_usuario.obtener_usuario_por_id_auth(user_id)
    user = None
    if userfrombd is not None:
        user = User(userfrombd[0], userfrombd[1], userfrombd[2])
    #return userid_table.get(user_id, None)
    return user

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'super-secret'

jwt = JWT(app, authenticate, identity)
app.secret_key = 'mysecretkey'


###### RUTAS USUARIO #####
###DECORADORES"""
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session or session.get('user_type') != 2:
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function



@app.route('/')
@app.route('/index')
def index():
    if 'cart' not in session:
        session['cart'] = {}

    productos = controlador_producto.obtener_productox3()
    pro1 = controlador_producto.aleatorio()
    pro2 = controlador_producto.aleatorio()
    pro3 = controlador_producto.aleatorio()
    pro4 = controlador_producto.aleatorio()
    return render_template('index.html', productos=productos, pro1=pro1, pro2=pro2, pro3=pro3, pro4=pro4)



@app.route('/mujer')
def mujer():
    productos = controlador_producto.obtener_productosMujer()
    return render_template('mujer.html', productos=productos)


@app.route('/carro_compra')
def carro_compra():
    return render_template('carro_compra.html')


@app.route('/acercade')
def acercade():
    return render_template('acerca_De.html')


@app.route('/contactos')
def contactos():
    return render_template('contactos.html')


@app.route('/hombre')
def hombre():
    productos = controlador_producto.obtener_productosHombre()
    return render_template('hombre.html', productos=productos)





@app.route('/registrarse')
def registrarse():
    return render_template('registrarse.html')


###### LEGALES #####


@app.route('/base_legales')
def base_legales():
    return render_template('datos_legales/base_legales.html')


@app.route('/cambios_devoluciones')
def cambios_devoluciones():
    return render_template('datos_legales/cambios_devoluciones.html')


@app.route('/politica_privacidad')
def politica_privacidad():
    return render_template('datos_legales/politica_privacidad.html')


@app.route('/preguntas_frecuentes')
def preguntas_frecuentes():
    return render_template('datos_legales/preguntas_frecuentes.html')


@app.route('/terminos_condiciones')
def terminos_condiciones():
    return render_template('datos_legales/terminos_condiciones.html')


###### RUTAS ADMINISTRADOR #####


@app.route('/admin_home')
@admin_required
def admin_home():
    try:
        con_user = controlador_usuario.contador_usuarios()
        con_productos = controlador_usuario.contador_productos()
        con_pedidos = controlador_usuario.contador_pedidos()
        con_pedidos_pendientes = controlador_usuario.contador_pedidos_pendientes()
        con_pedidos_enviados = controlador_usuario.contador_pedidos_enviados()
        con_productos_sin_stock = controlador_usuario.contador_producto_sin_stock()

        return render_template('administrador/dashboard.html',
                               con_user=con_user,
                               con_productos=con_productos,
                               con_pedidos=con_pedidos,
                               con_pedidos_pendientes=con_pedidos_pendientes,
                               con_pedidos_enviados=con_pedidos_enviados,
                               con_productos_sin_stock=con_productos_sin_stock)
    except Exception as e:
        logging.error(f"Error en admin_home: {e}")
        flash('Error al cargar el dashboard del administrador.')
        return redirect(url_for('login'))  # Redirigir al login en caso de error


# @app.route('/admin_user')
# def admin_user():
#     return render_template('administrador/botones_admini_user.html')
#Rutas para agregar, editar, actualizar, eliminar USUARIO


@app.route("/usuarios")
@admin_required
def usuarios():
    usuarios = controlador_usuario.obtener_usuarios()
    return render_template("administrador/usuarios.html", usuarios=usuarios)


@app.route("/agregar_usuario")
@admin_required
def formulario_agregar_usuario():
    tipos_usuario = controlador_usuario.obtener_nombre_tipo_usuario()
    # tipos_documento = controlador_usuario.obtener_nombre_tipo_documento()
    # print(tipos_documento)
    print(tipos_usuario)
    return render_template("administrador/agregar_usuario.html", tipos_usuario=tipos_usuario) #tipos_documento=tipos_documento




def fn_buscarDni(dni):


    dniBuscar = dni
    url_form = 'https://api.apis.net.pe/v2/reniec/dni?numero=' + dniBuscar
    token = "apis-token-8958.O758vEuKBUXkErNRgyLoM8dWrrkGJEOm"
    headers = {"Authorization": "Bearer " + token}

    try:
        response = requests.get(url_form, headers=headers )
        response.raise_for_status()  # Lanza una excepción para códigos de estado 4xx/5xx
        return response.json()
    except requests.exceptions.HTTPError as errh:
        print("Error HTTP:", errh)
    except requests.exceptions.ConnectionError as errc:
        print("Error de Conexión:", errc)
    except requests.exceptions.Timeout as errt:
        print("Error de Tiempo de Espera (Timeout):", errt)
    except requests.exceptions.RequestException as err:
        print("Error en la Solicitud API:", err)
    return {'error': 'Error al obtener los datos'}


@app.route('/agregar_dni')
@admin_required
def agregar_dni():
    return render_template('administrador/agregar_usuario_dni.html')

@app.route('/buscarDni', methods=['GET'])
@admin_required
def buscar_dni():
    dni = request.args.get('dni')
    if not dni:
        return jsonify({'error': 'No se proporcionó un DNI'}), 400

    usuario = fn_buscarDni(dni)
    if 'error' in usuario:
        return jsonify(usuario), 500

    return jsonify({
        'nombres': usuario.get('nombres', ''),
        'apellidoPaterno': usuario.get('apellidoPaterno', ''),
        'apellidoMaterno': usuario.get('apellidoMaterno', ''),


    })



@app.route("/guardar_usuario", methods=["POST"])
@admin_required
def guardar_usuario():
    #numeroDocumento= request.form["numeroDocumento"]
    nombre= request.form["nombres"]
    email = request.form["email"]
    telefono = request.form["telefono"]
    apellido = request.form["apellidos"]
    nombre_usuario = request.form["usuario"]
    contrasenia = request.form["contraseña"]
    fecha_nacimiento = request.form["fechaNacimiento"]
    tipo_usuario = request.form["id_TipoUsuario"]
    #tipo_documento = request.form["id_TipoDocumento"]
    controlador_usuario.insertar_usuario(nombre, email, telefono, apellido, nombre_usuario, contrasenia, fecha_nacimiento, tipo_usuario)
    # De cualquier modo, y si todo fue bien, redireccionar
    return redirect("/usuarios")

#Guardar Cliente:
@app.route("/guardar_cliente", methods=["POST"])
def guardar_cliente():
    #numeroDocumento= request.form["numeroDocumento"]
    nombre= request.form["nombres"]
    email = request.form["email"]
    telefono = request.form["telefono"]
    apellido = request.form["apellidos"]
    nombre_usuario = request.form["usuario"]
    contrasenia = request.form["contraseña"]
    fecha_nacimiento = None
    tipo_usuario = 1
    #tipo_documento = request.form["id_TipoDocumento"]
    controlador_usuario.insertar_usuario(nombre, email, telefono, apellido, nombre_usuario, contrasenia, fecha_nacimiento, tipo_usuario)
    # De cualquier modo, y si todo fue bien, redireccionar
    return redirect("/index")


@app.route("/eliminar_usuario", methods=["POST"])
@admin_required
def eliminar_usuario():
    controlador_usuario.eliminar_usuario(request.form["id"])
    return redirect("/usuarios")


@app.route("/formulario_editar_usuario/<int:id>")
@admin_required
def editar_usuario(id):
    # Obtener el usuario por ID
    tipos_usuario = controlador_usuario.obtener_nombre_tipo_usuario()
    #tipos_documento = controlador_usuario.obtener_nombre_tipo_documento()
    usuario = controlador_usuario.obtener_usuario_por_id(id)
    return render_template("administrador/editar_usuarios.html", usuario=usuario, tipos_usuario=tipos_usuario) #, tipos_documento=tipos_documento


@app.route("/actualizar_usuario", methods=["POST"])
@login_required
@admin_required
def actualizar_usuario():
    #numeroDocumento= request.form["numeroDocumento"]
    id = request.form["id"]
    nombre= request.form["nombres"]
    email = request.form["email"]
    telefono = request.form["telefono"]
    apellido = request.form["apellidos"]
    nombre_usuario = request.form["usuario"]
    contrasenia = request.form["contraseña"]
    fecha_nacimiento = request.form["fechaNacimiento"]
    #estado = request.form["status"]
    tipo_usuario = request.form["id_TipoUsuario"]
    #tipo_documento = request.form["id_TipoDocumento"]
    controlador_usuario.actualizar_usuario(nombre, email, telefono, apellido, nombre_usuario,contrasenia,fecha_nacimiento,tipo_usuario, id)
    return redirect("/usuarios")


@app.route('/verContactos/<int:id>')
@login_required
def verContactos(id):
    contactos = controlador_usuario.obtener_usuario_por_id(id)
    tarjetas = controlador_usuario.ver_tarjetas(id)
    return render_template('datos_personales/datos_personales.html', contactos=contactos, tar=tarjetas)

@app.route('/editarContactos_user/<int:id>', methods=['POST'])
@login_required
def editarContactos_user(id):
    nombre= request.form["nombre"]
    apellido = request.form["apellido"]
    email = request.form["email"]
    telefono = request.form["telefono"]
    password = request.form["password"]
    fechaNacimiento = request.form["fechaNacimiento"]
    controlador_usuario.actualizar_usuarioXuser(nombre,apellido, email, telefono,  password, fechaNacimiento, id)
    return redirect(url_for('verContactos', id=id))

@app.route('/id_a_agregar_tarjeta')
@login_required
def id_a_agregar_tarjeta():
    return render_template('datos_personales/agregar_tarjeta.html')

@app.route('/agregar_tarjetas', methods=['POST'])
@login_required
def agregar_tarjetas():
    numero_tarjeta = request.form['numero_tarjeta']
    nombre = request.form['titular']
    mes = request.form['mes']
    año = request.form['year']
    fecha_vencimiento =  año +'/'+ mes
    cvv = request.form['codigo_seguridad']
    controlador_usuario.agregar_tarjeta(numero_tarjeta, nombre,fecha_vencimiento, cvv, session['user_id'])
    return redirect(url_for('verContactos', id=session['user_id']))

@app.route('/ir_a_pagos/<int:id>')
@login_required
def ir_a_pagos(id):
    sub = controlador_usuario.detalle_pedido(id)
    ped = controlador_usuario.pago_pedido(id)
    tarjeta = controlador_usuario.ver_tarjetas(session['user_id'])
    print(ped)
    return render_template('pago.html', sub = sub , ped = ped, tarjeta = tarjeta)

@app.route('/pagar_pedidossssss/<int:id>', methods=['POST'])
@login_required
def pagar_pedidossssss(id):
    total = request.form['total']
    id_tarjeta = request.form['tarjeta']
    try:
        controlador_usuario.insertar_pago(id, id_tarjeta, total)
        flash('Pago realizado con éxito', 'success')
        return redirect(url_for('ver_pendientes'))
    except Exception as e:
        flash(f'No se pudo realizar el pago: {str(e)}', 'danger')
    return redirect(url_for('ver_pendientes'))


#Rutas para agregar, editar, actualizar, eliminar PRODUCTO

@app.route("/productos")
@admin_required
def productos():
    productos = controlador_producto.obtener_producto()
    return render_template("administrador/producto.html", productos=productos)


@app.route("/agregar_producto")
@admin_required
def formulario_agregar_producto():
    categorias = controlador_producto.obtener_nombre_categoria()
    print(categorias)
    return render_template("administrador/agregar_producto.html", categorias=categorias)



@app.route("/guardar_producto", methods=["POST"])
def guardar_producto():
    imagen = request.files.get('imagenes')
    if imagen and imagen.filename:
        nombre_imagen = secure_filename(imagen.filename)
        ruta_destino = os.path.join(app.root_path, 'static', 'assets' ,'img', 'productos', nombre_imagen)
        imagen.save(ruta_destino)
        ruta_imagen_db = os.path.join('img', 'productos', nombre_imagen).replace('\\', '/')
    else:
        ruta_imagen_db = 'img/productos/default.jpg'


    nombreProducto = request.form.get("nombreProducto", "")
    descripcion = request.form.get("descripcion", "")
    precio = request.form.get("precio", "0")
    stock = request.form.get("stock", "activo") #¿Cómo que activo?
    id_Categoria = request.form.get("id_Categoria", "1")
    genero = request.form.get("genero", "")
    talla = request.form.get("talla", "")

    controlador_producto.insertar_producto(nombreProducto, descripcion, precio, stock, id_Categoria, ruta_imagen_db, talla, genero)

    return redirect(url_for('productos'))



@app.route("/actualizar_producto", methods=["POST"])
def actualizar_producto():
    id = request.form["id"]
    imagen = request.form["imagen"]
    nombreProducto= request.form["nombreProducto"]
    descripcion = request.form["descripcion"]
    precio = request.form["precio"]
    stock = request.form["stock"]
    id_Categoria = request.form["id_Categoria"]
    talla = request.form["talla"]
    controlador_producto.actualizar_producto(nombreProducto, descripcion, precio,stock,id_Categoria, imagen, talla, id)
    return redirect("/productos")


@app.route("/eliminar_producto", methods=["POST"])
def eliminar_producto():
    controlador_producto.eliminar_producto(request.form["id"])
    return redirect("/productos")

@app.route("/formulario_editar_producto/<int:id>")
@admin_required
def editar_producto(id):
    # Obtener el usuario por ID
    producto = controlador_producto.obtener_producto_por_id(id)
    tipos_categorias = controlador_producto.obtener_nombre_categoria()
    return render_template("administrador/editar_producto.html", producto=producto, tipos_categorias = tipos_categorias)

@app.route('/producto_detalle/<int:id>')
@login_required
def producto_detalle(id):
    producto = controlador_producto.obtener_producto_por_id(id)
    if not producto:
        flash('Producto no encontrado')
        return redirect('/productos')
    return render_template('producto_detalle.html', producto=producto)



#PRUEBAS CARRITO



@app.route('/remove_from_cart', methods=['POST'])
@login_required
def remove_from_cart():
    product_id = request.form.get('product_id')
    if product_id in session.get('cart', {}):
        del session['cart'][product_id]
        session.modified = True
    return redirect(url_for('show_cart'))

@app.route('/clear_cart', methods=['POST'])
@login_required
def clear_cart():
    session['cart'] = {}
    session.modified = True
    return redirect(url_for('show_cart'))



@app.route('/add_to_cart', methods=['POST'])
@login_required
def add_to_cart():
    product_id = request.form.get('product_id')
    cantidad = int(request.form.get('cantidad', 1))

    if 'cart' not in session:
        session['cart'] = {}

    producto = controlador_producto.obtener_producto_por_id(int(product_id))

    if producto:
        stock_disponible = producto[4]

        # Verificar si la cantidad solicitada no excede el stock disponible
        if cantidad > stock_disponible:
            return jsonify({'message': 'Cantidad solicitada excede el stock disponible', 'cart': session.get('cart', {})})

        if product_id in session['cart']:
            nueva_cantidad = session['cart'][product_id]['cantidad'] + cantidad
            if nueva_cantidad > stock_disponible:
                return jsonify({'message': 'Cantidad total excede el stock disponible', 'cart': session.get('cart', {})})
            session['cart'][product_id]['cantidad'] = nueva_cantidad
        else:
            session['cart'][product_id] = {
                'id': producto[0],
                'nombre': producto[1],
                'precio': float(producto[3]),
                'cantidad': cantidad
            }

        session.modified = True
        return jsonify({'message': 'Producto añadido al carrito', 'cart': session['cart']})
    else:
        return jsonify({'message': 'Producto no encontrado', 'cart': session.get('cart', {})})



@app.route('/cart')
@login_required
def show_cart():
    cart = session.get('cart', {})
    total = sum(float(item['precio']) * item['cantidad'] for item in cart.values()) if cart else 0
    return render_template('carrito-prueba.html', cart=cart, total=total)

@app.route('/guardar_detalles', methods=['POST'])
def guardar_detalle():
    id_producto = request.form.getlist('id_producto[]')
    cantidad = request.form.getlist('cantidad[]')
    id_user = request.form['id_user']
    pedido_id = controlador_producto.insertar_nuevo_pedido(id_user)
    for i in range(len(id_producto)):
        controlador_producto.guardar_detalle(id_producto[i], cantidad[i], pedido_id)
    session['cart'] = {}
    return redirect(url_for('ver_pendientes'))

@app.route('/ver_pendientes')
@login_required
def ver_pendientes():
    try:
        pedidos = controlador_usuario.ver_pedidos_pendientes(session['user_id'])
        return render_template('datos_personales/pedidos_pendiente.html', pedidos=pedidos)
    except Exception as e:
        flash(f'Error al cargar los pedidos pendientes: {str(e)}', 'danger')
        return redirect(url_for('index'))

@app.route('/pagar_pedido/<int:id>')
@login_required
def pagar_pedido(id):
    controlador_usuario.pagar_pedido(id)
    return redirect(url_for('ver_pendientes'))

@app.route('/ver_historial')
@login_required
def ver_historial():
    try:
        pedidos = controlador_usuario.historial_pedido(session['user_id'])
        return render_template('historial_pedido.html', pedidos=pedidos)
    except Exception as e:
        flash(f'Error al cargar el historial de pedidos: {str(e)}', 'danger')
        return redirect(url_for('index'))

@app.route('/ver_detalle_pedido/<int:id>')
@login_required
def ver_detalle_pedido(id):
    detalle = controlador_usuario.historial_detalle_pedido(id)
    print(detalle)
    return render_template('detalle_pedido.html', detalle=detalle)


#############COOKIES
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        try:
            usuario = request.form['usuario']
            contrasenia = request.form['contrasenia']

            user = controlador_usuario.login(usuario, contrasenia)
            if user:
                session['logged_in'] = True
                session['user_type'] = user[0][0]
                session['user_id'] = user[0][1]
                session['user_name'] = user[0][2]
                session['token'] = user[0][3]
                session['email'] = user[0][4]

                aleatorio = str(random.randint(1, 1024))
                token = hashlib.sha256(aleatorio.encode("utf-8")).hexdigest()

                if session['user_type'] == 2:
                    response = make_response(redirect(url_for('admin_home')))
                else:
                    response = make_response(redirect(url_for('index')))

                response.set_cookie('email', session['email'])
                response.set_cookie('token', token)
                controlador_usuario.actualizar_token_usuario(usuario, token)

                flash('Login successful!')
                return response
            else:
                flash('Usuario o contraseña incorrectos')
                return redirect(url_for('index'))
        except Exception as e:
            logging.error(f"Error en login: {e}")
            flash('Error al procesar la solicitud.')
            return redirect(url_for('index'))
    else:
        # Si el método es GET, mostrar una página de login o redirigir
        return render_template('index.html')








@app.route('/logout')
def logout():
    session.clear()
    flash('Has cerrado sesión exitosamente.')
    resp = make_response(redirect(url_for('index')))
    resp.set_cookie('token', "", expires=0)
    resp.set_cookie('email', "", expires=0)
    return resp









#### APIS - USUARIOS ####



@app.route("/api_obtenerusuarios")
@jwt_required()
def api_obtenerusuarios():
    rpta = dict()
    try:
        listausuarios = []
        usuarios = controlador_usuario.obtener_usuarios()
        for usuario in usuarios:
            try:
                objUsuario = clase_usuario.clsUsuario(
                    usuario[0], usuario[1], usuario[2],
                    usuario[3], usuario[4], usuario[5],
                    usuario[6], usuario[7], usuario[8],
                    usuario[9]
                )
                listausuarios.append(objUsuario.diccusuario.copy())
            except Exception as e:
                print(f"Error procesando usuario: {e}")
        rpta["code"] = 1
        rpta["message"] = "Listado correcto de usuarios"
        rpta["data"] = listausuarios
        return jsonify(rpta)
    except Exception as e:
        rpta["code"] = 0
        rpta["message"] = f"Problemas en el servicio web: {e}"
        rpta["data"] = []
        return jsonify(rpta)

@app.route("/api_guardarusuario", methods=["POST"])
@jwt_required()
def api_guardarusuario():
    rpta=dict()
    try:
        nombre = request.json["nombre"]
        email = request.json["email"]
        telefono = request.json["telefono"]
        apellido = request.json["apellido"]
        nombre_usuario = request.json["nombredeusuario"]
        contraseña = request.json["contraseña"]
        fecha_nacimiento = request.json["fechaNacimiento"]
        tipo_Usuario = request.json["tipo_usuario_id"]
        idgenerado = controlador_usuario.insertar_usuario(nombre, email, telefono, apellido,
                                                          nombre_usuario, contraseña, fecha_nacimiento,tipo_Usuario)
        rpta["code"]=1
        rpta["message"]="Usuario registrado correctamente"
        rpta["data"]= {"idgenerado" : idgenerado}
    except Exception as e:
        rpta["code"]=0
        rpta["message"]="Ocurrió un problema: " + repr(e)
        rpta["data"]=dict()
    return rpta

@app.route("/api_actualizarusuario/<int:id>", methods=["PUT"])
@jwt_required()
def api_actualizarusuario(id):
    rpta = dict()
    try:
        nombre = request.json["nombre"]
        email = request.json["email"]
        telefono = request.json["telefono"]
        apellido = request.json["apellido"]
        nombre_usuario = request.json["nombredeusuario"]
        contraseña = request.json["contraseña"]
        fecha_nacimiento = request.json["fechaNacimiento"]
        tipo_Usuario = request.json["tipo_usuario_id"]
        controlador_usuario.actualizar_usuario(nombre, email, telefono, apellido,
                                               nombre_usuario, contraseña, fecha_nacimiento,
                                               tipo_Usuario, id)
        rpta["code"] = 1
        rpta["message"] = "Usuario actualizado correctamente"
    except Exception as e:
        rpta["code"] = 0
        rpta["message"] = "Ocurrió un problema: " + repr(e)
    return jsonify(rpta)

@app.route("/api_eliminarusuario/<int:id>", methods=["DELETE"])
@jwt_required()
def api_eliminarusuario(id):
    rpta = dict()
    try:
        usuario_eliminado = controlador_usuario.eliminar_usuario(id)
        if usuario_eliminado:
            rpta["code"] = 1
            rpta["message"] = "Usuario eliminado correctamente"
        else:
            rpta["code"] = 0
            rpta["message"] = "El usuario con el ID especificado no existe"
    except Exception as e:
        rpta["code"] = 0
        rpta["message"] = "Ocurrió un problema: " + repr(e)
    return jsonify(rpta)


#### APIS - PRODUCTO ####


@app.route("/api_obtenerproductos")
@jwt_required()
def api_obtenerproductos():
    rpta = dict()
    try:
        listaproductos = []
        productos = controlador_producto.obtener_producto()
        for producto in productos:
            try:
                objProducto = clase_producto.clsProducto(
                    producto[0], producto[1], producto[2],
                    producto[3], producto[4], producto[5],
                    producto[6], producto[7], producto[8],
                    producto[9]
                )
                listaproductos.append(objProducto.diccproducto.copy())
            except Exception as e:
                print(f"Error procesando producto: {e}")
        rpta["code"] = 1
        rpta["message"] = "Listado correcto de productos"
        rpta["data"] = listaproductos
        return jsonify(rpta)
    except Exception as e:
        rpta["code"] = 0
        rpta["message"] = f"Problemas en el servicio web: {e}"
        rpta["data"] = []
    return jsonify(rpta)

@app.route("/api_guardarproducto", methods=["POST"])
@jwt_required()
def api_guardarproducto():
    rpta = dict()
    try:
        nombre = request.json["nombre"]
        descripcion = request.json["descripcion"]
        precio = request.json["precio"]
        stock = request.json["stock"]
        id_categoria = request.json["categoria_id"]
        imagen = request.json["imagen"]
        talla = request.json["talla"]
        genero = request.json["genero"]
        idgenerado = controlador_producto.insertar_producto(nombre, descripcion, precio, stock,
                                               id_categoria, imagen, talla, genero)
        rpta["code"]=1
        rpta["message"]="Producto registrado correctamente"
        rpta["data"]= {"idgenerado" : idgenerado}
    except Exception as e:
        rpta["code"]=0
        rpta["message"]="Ocurrió un problema: " + repr(e)
        rpta["data"]=dict()
    return jsonify(rpta)

@app.route("/api_actualizarproducto/<int:id>", methods=["PUT"])
@jwt_required()
def api_actualizarproducto(id):
    rpta = dict()
    try:
        nombre = request.json["nombre"]
        descripcion = request.json["descripcion"]
        precio = request.json["precio"]
        stock = request.json["stock"]
        id_categoria = request.json["categoria_id"]
        imagen = request.json["imagen"]
        talla = request.json["talla"]

        producto_actualizado = controlador_producto.actualizar_producto(nombre, descripcion, precio, stock, id_categoria, imagen, talla, id)

        if producto_actualizado:
            rpta["code"] = 1
            rpta["message"] = "Producto actualizado correctamente"
        else:
            rpta["code"] = 0
            rpta["message"] = "El producto con el ID especificado no existe"
    except Exception as e:
        rpta["code"] = 0
        rpta["message"] = "Ocurrió un problema: " + repr(e)
    return jsonify(rpta)


@app.route("/api_eliminarproducto/<int:id>", methods=["DELETE"])
@jwt_required()
def api_eliminarproducto(id):
    rpta = dict()
    try:
        producto_eliminado = controlador_producto.eliminar_producto(id)
        if producto_eliminado:
            rpta["code"] = 1
            rpta["message"] = "Producto eliminado correctamente"
        else:
            rpta["code"] = 0
            rpta["message"] = "El producto con el ID especificado no existe"
    except Exception as e:
        rpta["code"] = 0
        rpta["message"] = "Ocurrió un problema: " + repr(e)
    return jsonify(rpta)



#### APIS - CATEGORIA ####


@app.route("/api_obtenercategoria")
@jwt_required()
def api_obtenercategoria():
    rpta = dict()
    try:
        listaproductos = []
        productos = controlador_producto.obtener_nombre_categoriaApi()
        for producto in productos:
            try:
                objProducto = clase_categoria.clsCategoria(
                    producto[0], producto[1], producto[2],
                    producto[3]
                )
                listaproductos.append(objProducto.diccateogoria.copy())
            except Exception as e:
                print(f"Error procesando producto: {e}")
        rpta["code"] = 1
        rpta["message"] = "Listado correcto de categorias"
        rpta["data"] = listaproductos
        return jsonify(rpta)
    except Exception as e:
        rpta["code"] = 0
        rpta["message"] = f"Problemas en el servicio web: {e}"
        rpta["data"] = []
    return jsonify(rpta)


@app.route("/api_obtenercategoria_x_id/<int:id>")
@jwt_required()
def api_obtenercategoria_x_id(id):
    rpta = dict()
    try:
        categorias = controlador_producto.obtener_nombre_categoriaApixid(id)
        if not categorias:
            rpta["code"] = 0
            rpta["message"] = "La categoría con el ID especificado no existe"
            rpta["data"] = []
            return jsonify(rpta)

        listacategorias = []
        for categoria in categorias:
            try:
                objCategoria = clase_categoria.clsCategoria(
                    categoria[0], categoria[1], categoria[2],
                    categoria[3]
                )
                listacategorias.append(objCategoria.diccateogoria.copy())
            except Exception as e:
                print(f"Error procesando categoria: {e}")
        rpta["code"] = 1
        rpta["message"] = "Listado correcto de categorías"
        rpta["data"] = listacategorias
        return jsonify(rpta)
    except Exception as e:
        rpta["code"] = 0
        rpta["message"] = f"Problemas en el servicio web: {e}"
        rpta["data"] = []
    return jsonify(rpta)


@app.route("/api_guardarcategoria", methods=["POST"])
@jwt_required()
def api_guardarcategoria():
    rpta = dict()
    try:
        nombre = request.json["nombre"]
        descripcion = request.json["descripcion"]
        fecha_creacion = request.json["fecha_creacion"]
        idgenerado = controlador_producto.insertar_categoria(nombre, descripcion,fecha_creacion)

        rpta["code"]=1
        rpta["message"]="Categoria registrado correctamente"
        rpta["data"]= {"idgenerado" : idgenerado}
    except Exception as e:
        rpta["code"]=0
        rpta["message"]="Ocurrió un problema: " + repr(e)
        rpta["data"]=dict()
    return jsonify(rpta)


@app.route("/api_actualizarcategoria/<int:id>", methods=["PUT"])
@jwt_required()
def api_actualizarcategoria(id):
    rpta = dict()
    try:
        nombre = request.json["nombre"]
        descripcion = request.json["descripcion"]
        fecha_creacion = request.json["fecha_creacion"]

        categoria_actualizada = controlador_producto.actualizar_categoria(nombre, descripcion, fecha_creacion, id)

        if categoria_actualizada:
            rpta["code"] = 1
            rpta["message"] = "Categoría actualizada correctamente"
        else:
            rpta["code"] = 0
            rpta["message"] = "La categoría con el ID especificado no existe"
    except Exception as e:
        rpta["code"] = 0
        rpta["message"] = "Ocurrió un problema: " + repr(e)
    return jsonify(rpta)



@app.route("/api_eliminarcategoria/<int:id>", methods=["DELETE"])
@jwt_required()
def api_eliminarcategoria(id):
    rpta = dict()
    try:
        categoria_eliminada = controlador_producto.eliminar_categoria(id)
        if categoria_eliminada:
            rpta["code"] = 1
            rpta["message"] = "Categoría eliminada correctamente"
        else:
            rpta["code"] = 0
            rpta["message"] = "La categoría con el ID especificado no existe"
    except Exception as e:
        rpta["code"] = 0
        rpta["message"] = "Ocurrió un problema: " + repr(e)
    return jsonify(rpta)


##API TIPO USUARIO

@app.route("/api_obtenertipousuario")
@jwt_required()
def api_obtenertipousuario():
    rpta = dict()
    try:
        listausuarios = []
        usuarios = controlador_usuario.obtener_nombre_tipo_usuario()
        for usuario in usuarios:
            try:
                objUsuario = clase_tipo_usuario.clsTipoUser(
                    usuario[0], usuario[1]
                )
                listausuarios.append(objUsuario.diccateogoria.copy())
            except Exception as e:
                print(f"Error procesando usuario: {e}")
        rpta["code"] = 1
        rpta["message"] = "Listado correcto de usuarios"
        rpta["data"] = listausuarios
        return jsonify(rpta)
    except Exception as e:
        rpta["code"] = 0
        rpta["message"] = f"Problemas en el servicio web: {e}"
        rpta["data"] = []
    return jsonify(rpta)

@app.route("/api_obtenertipousuario_x_id/<int:id>")
@jwt_required()
def api_obtenertipousuario_x_id(id):
    rpta = dict()
    try:
        usuarios = controlador_usuario.obtener_nombre_tipo_usuario_x_id(id)
        if not usuarios:
            rpta["code"] = 0
            rpta["message"] = "El tipo de usuario con el ID especificado no existe"
            rpta["data"] = []
            return jsonify(rpta)

        listausuarios = []
        for usuario in usuarios:
            try:
                objUsuario = clase_tipo_usuario.clsTipoUser(
                    usuario[0], usuario[1]
                )
                listausuarios.append(objUsuario.diccateogoria.copy())
            except Exception as e:
                print(f"Error procesando usuario: {e}")
        rpta["code"] = 1
        rpta["message"] = "Listado correcto de usuarios"
        rpta["data"] = listausuarios
        return jsonify(rpta)
    except Exception as e:
        rpta["code"] = 0
        rpta["message"] = f"Problemas en el servicio web: {e}"
        rpta["data"] = []
    return jsonify(rpta)


@app.route("/api_guardartipousuario", methods=["POST"])
@jwt_required()
def api_guardartipousuario():
    rpta = dict()
    try:
        nombre = request.json["nombre"]
        idgenerado = controlador_usuario.insertar_tipo_usuario(nombre)

        rpta["code"]=1
        rpta["message"]="Tipo Usuario registrado correctamente"
        rpta["data"]= {"idgenerado" : idgenerado}
    except Exception as e:
        rpta["code"]=0
        rpta["message"]="Ocurrió un problema: " + repr(e)
        rpta["data"]=dict()
    return jsonify(rpta)

@app.route("/api_actualizartipousuario/<int:id>", methods=["PUT"])
@jwt_required()
def api_actualizartipousuario(id):
    rpta = dict()
    try:
        nombre = request.json["nombre"]
        tipo_usuario_actualizado = controlador_usuario.actualizar_tipo_usuario(nombre, id)

        if tipo_usuario_actualizado:
            rpta["code"] = 1
            rpta["message"] = "Tipo de usuario actualizado correctamente"
        else:
            rpta["code"] = 0
            rpta["message"] = "El tipo de usuario con el ID especificado no existe"
    except Exception as e:
        rpta["code"] = 0
        rpta["message"] = "Ocurrió un problema: " + repr(e)
    return jsonify(rpta)


@app.route("/api_eliminartipousuario/<int:id>", methods=["DELETE"])
@jwt_required()
def api_eliminartipousuario(id):
    rpta = dict()
    try:
        tipo_usuario_eliminado = controlador_usuario.eliminar_tipo_usuario(id)
        if tipo_usuario_eliminado:
            rpta["code"] = 1
            rpta["message"] = "Tipo de usuario eliminado correctamente"
        else:
            rpta["code"] = 0
            rpta["message"] = "El tipo de usuario con el ID especificado no existe"
    except Exception as e:
        rpta["code"] = 0
        rpta["message"] = "Ocurrió un problema: " + repr(e)
    return jsonify(rpta)



#### api tarjeta

@app.route("/api_obtenertarjeta")
@jwt_required()
def api_obtenertarjeta():
    rpta = dict()
    try:
        listausuarios = []
        usuarios = controlador_usuario.obtener_tajerta()
        for usuario in usuarios:
            try:
                objUsuario = clase_tarjeta.clsTajetas(
                    usuario[0], usuario[1], usuario[2],
                    usuario[3], usuario[4], usuario[5]
                )
                listausuarios.append(objUsuario.dictajeta.copy())
            except Exception as e:
                print(f"Error procesando usuario: {e}")
                # TOTAL DE TARJETAS
        rpta["code"] = 1
        rpta["message"] = "Listado correcto de usuarios"
        rpta["data"] = listausuarios
        return jsonify(rpta)
    except Exception as e:
        rpta["code"] = 0
        rpta["message"] = f"Problemas en el servicio web: {e}"
        rpta["data"] = []
    return jsonify(rpta)

@app.route("/api_obtenertarjeta_x_id/<int:id>")
@jwt_required()
def api_obtenertarjeta_x_id(id):
    rpta = dict()
    try:
        usuarios = controlador_usuario.api_ver_tarjetas(id)
        if not usuarios:
            rpta["code"] = 0
            rpta["message"] = "No se encontraron tarjetas con el ID especificado"
            rpta["data"] = []
            return jsonify(rpta)

        listausuarios = []
        for usuario in usuarios:
            try:
                objUsuario = clase_tarjeta.clsTajetas(
                    usuario[0], usuario[1], usuario[2],
                    usuario[3], usuario[4], usuario[5]
                )
                listausuarios.append(objUsuario.dictajeta.copy())
            except Exception as e:
                print(f"Error procesando usuario: {e}")
        rpta["code"] = 1
        rpta["message"] = "Listado correcto de tarjetas"
        rpta["data"] = listausuarios
        return jsonify(rpta)
    except Exception as e:
        rpta["code"] = 0
        rpta["message"] = f"Problemas en el servicio web: {e}"
        rpta["data"] = []
    return jsonify(rpta)


@app.route("/api_guardartarjeta", methods=["POST"])
@jwt_required()
def api_guardartarjeta():
    rpta = dict()
    try:
        numero_tarjeta = request.json["numero_tarjeta"]
        nombre = request.json["nombre"]
        fecha_vencimiento = request.json["fecha_vencimiento"]
        cvv = request.json["cvv"]
        id_user = request.json["id_user"]
        idgenerado = controlador_usuario.agregar_tarjeta(numero_tarjeta, nombre, fecha_vencimiento, cvv, id_user)

        rpta["code"]=1
        rpta["message"]="Tarjeta registrado correctamente"
        rpta["data"]= {"idgenerado" : idgenerado}
    except Exception as e:
        rpta["code"]=0
        rpta["message"]="Ocurrió un problema: " + repr(e)
        rpta["data"]=dict()
    return jsonify(rpta)

@app.route("/api_actualizartarjeta/<int:id>", methods=["PUT"])
@jwt_required()
def api_actualizartarjeta(id):
    rpta = dict()
    try:
        numero_tarjeta = request.json["numero_tarjeta"]
        nombre = request.json["nombre"]
        fecha_vencimiento = request.json["fecha_vencimiento"]
        codigo_seguridad = request.json["codigo_seguridad"]
        id_user = request.json["id_user"]

        tarjeta_actualizada = controlador_usuario.actualizar_tarjeta(numero_tarjeta, nombre, fecha_vencimiento, codigo_seguridad, id_user, id)

        if tarjeta_actualizada:
            rpta["code"] = 1
            rpta["message"] = "Tarjeta actualizada correctamente"
        else:
            rpta["code"] = 0
            rpta["message"] = "La tarjeta con el ID especificado no existe"
    except Exception as e:
        rpta["code"] = 0
        rpta["message"] = "Ocurrió un problema: " + repr(e)
    return jsonify(rpta)


@app.route("/api_eliminartarjeta/<int:id>", methods=["DELETE"])
@jwt_required()
def api_eliminartarjeta(id):
    rpta = dict()
    try:
        tarjeta_eliminada = controlador_usuario.eliminar_tarjeta(id)
        if tarjeta_eliminada:
            rpta["code"] = 1
            rpta["message"] = "Tarjeta eliminada correctamente"
        else:
            rpta["code"] = 0
            rpta["message"] = "La tarjeta con el ID especificado no existe"
    except Exception as e:
        rpta["code"] = 0
        rpta["message"] = "Ocurrió un problema: " + repr(e)
    return jsonify(rpta)


#### api direccion

@app.route("/api_obtenerdireccion")
@jwt_required()
def api_obtenerdireccion():
    rpta = dict()
    try:
        listausuarios = []
        usuarios = controlador_usuario.obtener_direccion()
        for usuario in usuarios:
            try:
                objUsuario = clase_direccion.clsDireccion(
                    usuario[0], usuario[1], usuario[2],
                    usuario[3], usuario[4], usuario[5],
                    usuario[6], usuario[7]
                )
                listausuarios.append(objUsuario.dicdireccion.copy())
            except Exception as e:
                print(f"Error procesando usuario: {e}")
                # TOTAL DE TARJETAS
        rpta["code"] = 1
        rpta["message"] = "Listado correcto de usuarios"
        rpta["data"] = listausuarios
        return jsonify(rpta)
    except Exception as e:
        rpta["code"] = 0
        rpta["message"] = f"Problemas en el servicio web: {e}"
        rpta["data"] = []
    return jsonify(rpta)

@app.route("/api_obtenerdireccion_x_id/<int:id>")
@jwt_required()
def api_obtenerdireccion_x_id(id):
    rpta = dict()
    try:
        listausuarios = []
        usuarios = controlador_usuario.obtener_direccion_por_id(id)
        for usuario in usuarios:
            try:
                objUsuario = clase_direccion.clsDireccion(
                    usuario[0], usuario[1], usuario[2],
                    usuario[3], usuario[4], usuario[5],
                    usuario[6], usuario[7]
                )
                listausuarios.append(objUsuario.dicdireccion.copy())
            except Exception as e:
                print(f"Error procesando usuario: {e}")
        rpta["code"] = 1
        rpta["message"] = "Listado correcto de direcciones"
        rpta["data"] = listausuarios
        return jsonify(rpta)
    except Exception as e:
        rpta["code"] = 0
        rpta["message"] = f"Problemas en el servicio web: {e}"
        rpta["data"] = []
    return jsonify(rpta)

@app.route("/api_guardardireccion", methods=["POST"])
@jwt_required()
def api_guardardireccion():
    rpta = dict()
    try:
        pais = request.json["pais"]
        departamento = request.json["departamento"]
        ciudad = request.json["ciudad"]
        codigo_postal = request.json["codigo_postal"]
        direccion1 = request.json["direccion1"]
        direccion2 = request.json["direccion2"]
        usuarios_id = request.json["usuarios_id"]
        idgenerado = controlador_usuario.insertar_direccion( pais, departamento, ciudad, codigo_postal, direccion1, direccion2, usuarios_id)

        rpta["code"]=1
        rpta["message"]="Direccion registrado correctamente"
        rpta["data"]= {"idgenerado" : idgenerado}
    except Exception as e:
        rpta["code"]=0
        rpta["message"]="Ocurrió un problema: " + repr(e)
        rpta["data"]=dict()
    return jsonify(rpta)

@app.route("/api_actualizardireccion/<int:id>", methods=["PUT"])
@jwt_required()
def api_actualizardireccion(id):
    rpta = dict()
    try:
        pais = request.json["pais"]
        departamento = request.json["departamento"]
        ciudad = request.json["ciudad"]
        codigo_postal = request.json["codigo_postal"]
        direccion1 = request.json["direccion1"]
        direccion2 = request.json["direccion2"]
        usuarios_id = request.json["usuarios_id"]
        id = controlador_usuario.actualizar_direccion(pais, departamento, ciudad, codigo_postal, direccion1, direccion2, usuarios_id, id)
        rpta["code"] = id
        rpta["message"] = "Direccion actualizado correctamente"
    except Exception as e:
        rpta["code"] = 0
        rpta["message"] = "Ocurrió un problema: " + repr(e)
    return jsonify(rpta)

@app.route("/api_eliminardireccion/<int:id>", methods=["DELETE"])
@jwt_required()
def api_eliminardireccion(id):
    rpta = dict()
    try:
        controlador_usuario.eliminar_direccion(id)
        rpta["code"] = 1
        rpta["message"] = "Direccion eliminado correctamente"
    except Exception as e:
        rpta["code"] = 0
        rpta["message"] = "Ocurrió un problema: " + repr(e)
    return jsonify(rpta)


#### api pagos
@app.route("/api_obtenerpagos", methods=["GET"])
@jwt_required()
def api_obtenerpagos():
    rpta = dict()
    try:
        listausuarios = []
        usuarios = controlador_usuario.api_pago()
        for usuario in usuarios:
            try:
                objUsuario = clase_pago.clsPago(
                    usuario[0], usuario[1], usuario[2],
                    usuario[3], usuario[4], usuario[5]
                )
                listausuarios.append(objUsuario.dicpago.copy())
            except Exception as e:
                print(f"Error procesando usuario: {e}")
                # TOTAL DE TARJETAS
        rpta["code"] = 1
        rpta["message"] = "Listado correcto de pagos"
        rpta["data"] = listausuarios
        return jsonify(rpta)
    except Exception as e:
        rpta["code"] = 0
        rpta["message"] = f"Problemas en el servicio web: {e}"
        rpta["data"] = []
    return jsonify(rpta)

@app.route("/api_obtenerpagos_x_id/<int:id>")
@jwt_required()
def api_obtenerpagos_x_id(id):
    rpta = dict()
    try:
        listausuarios = []
        usuarios = controlador_usuario.api_pago_por_id(id)
        for usuario in usuarios:
            try:
                objUsuario = clase_pago.clsPago(
                    usuario[0], usuario[1], usuario[2],
                    usuario[3], usuario[4], usuario[5]
                )
                listausuarios.append(objUsuario.dicpago.copy())
            except Exception as e:
                print(f"Error procesando usuario: {e}")
        rpta["code"] = 1
        rpta["message"] = "Listado correcto de pago"
        rpta["data"] = listausuarios
        return jsonify(rpta)
    except Exception as e:
        rpta["code"] = 0
        rpta["message"] = f"Problemas en el servicio web: {e}"
        rpta["data"] = []
    return jsonify(rpta)

@app.route("/api_guardarpagos", methods=["POST"])
@jwt_required()
def api_guardarpagos():
    rpta = dict()
    try:
        pedido = request.json["pedido"]
        tarjeta_id = request.json["tarjeta_id"]
        total_pago = request.json["total"]
        idgenerado = controlador_usuario.insertar_pago_return(pedido, tarjeta_id ,total_pago)

        rpta["code"]=1
        rpta["message"]="Pago registrado correctamente"
        rpta["data"]= {"idgenerado" : idgenerado}
    except Exception as e:
        rpta["code"]=0
        rpta["message"]="Ocurrió un problema: " + repr(e)
        rpta["data"]=dict()
    return jsonify(rpta)

@app.route("/api_actualizarpagos/<int:id>", methods=["PUT"])
@jwt_required()
def api_actualizarpagos(id):
    rpta = dict()
    try:
        fecha = request.json["fecha"]
        total = request.json["total"]
        tarjeta_id = request.json["tarjeta_id"]
        pedido_id = request.json["pedido"]
        controlador_usuario.actualizar_pago(fecha, total, pedido_id ,tarjeta_id, id)
        rpta["code"] = id
        rpta["message"] = "Pago actualizado correctamente"
    except Exception as e:
        rpta["code"] = 0
        rpta["message"] = "Ocurrió un problema: " + repr(e)
    return jsonify(rpta)

@app.route("/api_eliminarpagos/<int:id>", methods=["DELETE"])
@jwt_required()
def api_eliminarpagos(id):
    rpta = dict()
    try:
        controlador_usuario.eliminar_pago(id)
        rpta["code"] = 1
        rpta["message"] = "Pago eliminado correctamente"
    except Exception as e:
        rpta["code"] = 0
        rpta["message"] = "Ocurrió un problema: " + repr(e)
    return jsonify(rpta)





####CRUDS
@app.route('/admin_crud')
@admin_required
def admin_crud():
    return render_template('administrador/INT_CRUDS.html')

###TARJETA

@app.route('/admin_crud_tarjeta_general')
@admin_required
def admin_crud_tarjeta_general():
    usuarios = controlador_usuario.obtener_mantenimiento_tarjeta()
    return render_template('CRUDS/TARJETAS/general.html', usuarios=usuarios)

@app.route('/admin_crud_insertar_tarjeta')
@admin_required
def admin_crud_insertar_tarjeta():
    obo = controlador_usuario.obtener_usuarios()
    return render_template('CRUDS/TARJETAS/insert.html', obo=obo)

@app.route('/admin_crud_actualizar_tarjeta/<int:id>')
@admin_required
def admin_crud_actualizar_tarjeta(id):
    usuario = controlador_usuario.obtener_mantenimiento_tarjeta_x_id(id)
    return render_template('CRUDS/TARJETAS/actualizar.html', usuario=usuario)

@app.route('/admin_crud_actualizar_tarjeta_completa' , methods=['POST'])
@admin_required
def admin_crud_actualizar_tarjeta_completa():
    id = request.form["id"]
    nombre= request.form["nombres"]
    email = request.form["email"]
    telefono = request.form["telefono"]
    apellido = request.form["apellidos"]
    nombre_usuario = request.form["usuario"]
    id_usu = request.form["id_usu"]
    controlador_usuario.actualizar_tarjeta(email,telefono,apellido,nombre_usuario, id_usu ,id)
    return redirect("/admin_crud_tarjeta_general")


@app.route('/admin_crud_insert_tarjeta', methods=['POST'])
@admin_required
def admin_crud_insert_tarjeta():

    email = request.form["nombres"]
    telefono = request.form["apellidos"]
    apellido = request.form["email"]
    nombre_usuario = request.form["telefono"]
    usuario = request.form["usuario"]
    if controlador_usuario.agregar_tarjeta(email,telefono,apellido,nombre_usuario, usuario):
        flash('Tarjeta agregada correctamente')
        return redirect('/admin_crud_tarjeta_general')
    flash('Error al agregar la tarjeta')
    return redirect('/admin_crud_tarjeta_general')

@app.route('/admin_crud_eliminar_tarjeta', methods=['POST'])
@admin_required
def admin_crud_eliminar_tarjeta():
    controlador_usuario.eliminar_tarjeta(request.form["id"])
    return redirect("/admin_crud_tarjeta_general")








##DIRECCION


@app.route('/admin_crud_direccion_general')
@admin_required
def admin_crud_direccion_general():
    usuarios = controlador_usuario.obtener_direccion_MANTENIMIENTO()
    return render_template('CRUDS/DIRECCION/general.html', usuarios=usuarios)

@app.route('/admin_crud_insertar_direccion')
@admin_required
def admin_crud_insertar_direccion():
    obo = controlador_usuario.obtener_usuarios()
    return render_template('CRUDS/DIRECCION/insert.html', obo=obo)

@app.route('/admin_crud_actualizar_direccion/<int:id>')
@admin_required
def admin_crud_actualizar_direccion(id):
    usuario = controlador_usuario.obtener_direccion_id_MANTENIMIENTO(id)
    return render_template('CRUDS/DIRECCION/actualizar.html', usuario=usuario)

@app.route('/admin_crud_actualizar_direccion_completa' , methods=['POST'])
@admin_required
def admin_crud_actualizar_direccion_completa():
    id = request.form["id"]
    nombre= request.form["nombres"]
    email = request.form["email"]
    telefono = request.form["telefono"]
    apellido = request.form["apellidos"]
    nombre_usuario = request.form["usuario"]
    direccion = request.form["direccion"]
    id_usu = request.form["id_usu"]
    controlador_usuario.actualizar_direccion(nombre,email,telefono,apellido,nombre_usuario, direccion ,id_usu ,id)
    return redirect("/admin_crud_direccion_general")


@app.route('/admin_crud_insert_direccion', methods=['POST'])
@admin_required
def admin_crud_insert_direccion():

    email = request.form["nombres"]
    telefono = request.form["apellidos"]
    apellido = request.form["email"]
    nombre_usuario = request.form["telefono"]
    direccion_1 = request.form["direccion_1"]
    direccion_2 = request.form["direccion_2"]
    usuario = request.form["usuario"]
    if controlador_usuario.insertar_direccion(email,telefono,apellido,nombre_usuario, direccion_1, direccion_2 ,usuario):
        flash('direccion agregada correctamente')
        return redirect('/admin_crud_direccion_general')
    flash('Error al agregar la direccion')
    return redirect('/admin_crud_direccion_general')

@app.route('/admin_crud_eliminar_direccion', methods=['POST'])
@admin_required
def admin_crud_eliminar_direccion():
    controlador_usuario.eliminar_direccion(request.form["id"])
    return redirect("/admin_crud_direccion_general")



########categorias

@app.route('/admin_crud_categoria_general')
@admin_required
def admin_crud_categoria_general():
    usuarios = controlador_producto.obtener_nombre_categoriaApi()
    return render_template('CRUDS/CATEGORIAS/general.html', usuarios=usuarios)

@app.route('/admin_crud_insertar_categoria')
@admin_required
def admin_crud_insertar_categoria():
    obo = controlador_usuario.obtener_usuarios()
    return render_template('CRUDS/CATEGORIAS/insert.html', obo=obo)

@app.route('/admin_crud_actualizar_categoria/<int:id>')
@admin_required
def admin_crud_actualizar_categoria(id):
    usuario = controlador_producto.obtener_nombre_categoriaApixid(id)
    return render_template('CRUDS/CATEGORIAS/actualizar.html', usuario=usuario)

@app.route('/admin_crud_actualizar_categoria_completa' , methods=['POST'])
@admin_required
def admin_crud_actualizar_categoria_completa():
    id = request.form["id"]
    nombre = request.form["nombre"]
    descripcion = request.form["descripcion"]
    fecha_creacion = request.form["fecha_creacion"]
    filas_actualizadas = controlador_producto.actualizar_categoria(nombre, descripcion, fecha_creacion, id)
    if filas_actualizadas:
        flash("Categoria actualizada correctamente", "success")
    else:
        flash("No se pudo actualizar la categoría", "error")
    return redirect("/admin_crud_categoria_general")


@app.route('/admin_crud_insert_categoria', methods=['POST'])
@admin_required
def admin_crud_insert_categoria():
    nombre = request.form["nombre"]
    descripcion = request.form["descripcion"]
    fecha_creacion = request.form["fecha_creacion"]
    nuevo_id = controlador_producto.insertar_categoria(nombre, descripcion, fecha_creacion)
    if nuevo_id:
        flash("Categoría agregada correctamente", "success")
    else:
        flash("Error al agregar la categoría", "error")
    return redirect('/admin_crud_categoria_general')

@app.route('/admin_crud_eliminar_categoria', methods=['POST'])
@admin_required
def admin_crud_eliminar_categoria():
    controlador_producto.eliminar_categoria(request.form["id"])
    return redirect("/admin_crud_categoria_general")






########tipo usuario

@app.route('/admin_crud_tipo_user_general')
@admin_required
def admin_crud_tipo_user_general():
    usuarios = controlador_usuario.obtener_nombre_tipo_usuario()
    return render_template('CRUDS/TIPO USUARIO/general.html', usuarios=usuarios)

@app.route('/admin_crud_insertar_tipo_user')
@admin_required
def admin_crud_insertar_tipo_user():
    obo = controlador_usuario.obtener_usuarios()
    return render_template('CRUDS/TIPO USUARIO/insert.html', obo=obo)

@app.route('/admin_crud_actualizar_tipo_user/<int:id>')
@admin_required
def admin_crud_actualizar_tipo_user(id):
    usuario = controlador_usuario.obtener_nombre_tipo_usuario_x_idA(id)
    return render_template('CRUDS/TIPO USUARIO/actualizar.html', usuario=usuario)

@app.route('/admin_crud_actualizar_tipo_user_completa' , methods=['POST'])
@admin_required
def admin_crud_actualizar_tipo_user_completa():
    id = request.form["id"]
    nombre= request.form["nombres"]


    controlador_usuario.actualizar_tipo_usuario(nombre, id)
    return redirect("/admin_crud_tipo_user_general")


@app.route('/admin_crud_insert_tipo_user', methods=['POST'])
@admin_required
def admin_crud_insert_tipo_user():

    email = request.form["nombres"]


    if controlador_usuario.insertar_tipo_usuario(email):
        flash('tipo usuario agregada correctamente')
        return redirect('/admin_crud_tipo_user_general')
    flash('Error al agregar tipo usuario')
    return redirect('/admin_crud_tipo_user_general')

@app.route('/admin_crud_eliminar_tipo_user', methods=['POST'])
@admin_required
def admin_crud_eliminar_tipo_user():
    controlador_usuario.eliminar_tipo_usuario(request.form["id"])
    return redirect("/admin_crud_tipo_user_general")



@app.route('/admin_crud_pedido_enviado_general')
@admin_required
def admin_crud_pedido_enviado_general():
    usuarios = controlador_usuario.ver_pedidos_general_enviados()
    return render_template('CRUDS/ENVIADOS/general.html', usuarios=usuarios)



@app.route('/admin_crud_pedido_PENDIENTE_general')
@admin_required
def admin_crud_pedido_PENDIENTE_general():
    usuarios = controlador_usuario.ver_pedidos_general_PENDIENTE()
    return render_template('CRUDS/PENDIENTES/general.html', usuarios=usuarios)







if __name__ == '__main__':
    app.run(debug=True)
