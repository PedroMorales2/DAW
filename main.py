from flask import Flask, render_template, request, redirect, flash, jsonify, session, url_for
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash
import os
import controlador_producto
import controlador_usuario
import requests
app = Flask(__name__)

app.secret_key = 'mysecretkey'

###### RUTAS USUARIO #####

@app.route('/')
@app.route('/index')
def index():
    if 'cart' not in session:
        session['cart'] = {}
    return render_template('index.html')



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
def admin_home():
    return render_template('administrador/admin_home.html')

# @app.route('/admin_user')
# def admin_user():
#     return render_template('administrador/botones_admini_user.html')
#Rutas para agregar, editar, actualizar, eliminar USUARIO


@app.route("/usuarios")
def usuarios():
    usuarios = controlador_usuario.obtener_usuarios()
    return render_template("administrador/usuarios.html", usuarios=usuarios)


@app.route("/agregar_usuario")
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
        response = requests.get(url_form, headers=headers)
        response.raise_for_status()  # Lanza una excepción para códigos de estado 4xx/5xx
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error en la solicitud API: {e}")
        return {'error': 'Error al obtener los datos'}


@app.route('/agregar_dni')
def agregar_dni():
    return render_template('administrador/agregar_usuario_dni.html')

@app.route('/buscarDni', methods=['GET'])
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
def eliminar_usuario():
    controlador_usuario.eliminar_usuario(request.form["id"])
    return redirect("/usuarios")


@app.route("/formulario_editar_usuario/<int:id>")
def editar_usuario(id):
    # Obtener el usuario por ID
    tipos_usuario = controlador_usuario.obtener_nombre_tipo_usuario()
    #tipos_documento = controlador_usuario.obtener_nombre_tipo_documento()
    usuario = controlador_usuario.obtener_usuario_por_id(id)
    return render_template("administrador/editar_usuarios.html", usuario=usuario, tipos_usuario=tipos_usuario) #, tipos_documento=tipos_documento


@app.route("/actualizar_usuario", methods=["POST"])
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
def verContactos(id):
    contactos = controlador_usuario.obtener_usuario_por_id(id)
    tarjetas = controlador_usuario.ver_tarjetas(id)
    return render_template('datos_personales/datos_personales.html', contactos=contactos, tar=tarjetas)       

@app.route('/editarContactos_user/<int:id>', methods=['POST'])
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
def id_a_agregar_tarjeta():
    return render_template('datos_personales/agregar_tarjeta.html')
   
@app.route('/agregar_tarjetas', methods=['POST'])
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
def ir_a_pagos(id):
    sub = controlador_usuario.detalle_pedido(id)
    ped = controlador_usuario.pago_pedido(id)
    tarjeta = controlador_usuario.ver_tarjetas(session['user_id'])
    print(ped)
    return render_template('pago.html', sub = sub , ped = ped, tarjeta = tarjeta)

@app.route('/pagar_pedidossssss/<int:id>', methods=['POST'])
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
def productos():
    productos = controlador_producto.obtener_producto()
    return render_template("administrador/producto.html", productos=productos)


@app.route("/agregar_producto")
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
def editar_producto(id):
    # Obtener el usuario por ID
    producto = controlador_producto.obtener_producto_por_id(id)
    tipos_categorias = controlador_producto.obtener_nombre_categoria()
    return render_template("administrador/editar_producto.html", producto=producto, tipos_categorias = tipos_categorias)
@app.route('/producto_detalle/<int:id>')
def producto_detalle(id):
    producto = controlador_producto.obtener_producto_por_id(id)
    if not producto:
        flash('Producto no encontrado')
        return redirect('/productos')  
    return render_template('producto_detalle.html', producto=producto)



#PRUEBAS CARRITO 



@app.route('/remove_from_cart', methods=['POST'])
def remove_from_cart():
    product_id = request.form.get('product_id')
    if product_id in session.get('cart', {}):
        del session['cart'][product_id]
        session.modified = True
    return redirect(url_for('show_cart'))

@app.route('/clear_cart', methods=['POST'])
def clear_cart():
    session['cart'] = {}
    session.modified = True
    return redirect(url_for('show_cart'))



@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    product_id = request.form.get('product_id')
    cantidad = int(request.form.get('cantidad', 1))  

    if 'cart' not in session:
        session['cart'] = {}

    if product_id in session['cart']:
        session['cart'][product_id]['cantidad'] += cantidad
    else:
        producto = controlador_producto.obtener_producto_por_id(int(product_id))
        if producto:
            session['cart'][product_id] = {
                'id' : producto[0],
                'nombre': producto[1],
                'precio': float(producto[3]), 
                'cantidad': cantidad
            }

    session.modified = True
    return jsonify({'message': 'Producto añadido al carrito', 'cart': session['cart']})



@app.route('/cart')
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
def ver_pendientes():
    try:    
        pedidos = controlador_usuario.ver_pedidos_pendientes(session['user_id'])
        return render_template('datos_personales/pedidos_pendiente.html', pedidos=pedidos)
    except Exception as e:
        flash(f'Error al cargar los pedidos pendientes: {str(e)}', 'danger')
        return redirect(url_for('index'))
    
@app.route('/pagar_pedido/<int:id>')
def pagar_pedido(id):
    controlador_usuario.pagar_pedido(id)
    return redirect(url_for('ver_pendientes'))

@app.route('/ver_historial')
def ver_historial():
    try: 
        pedidos = controlador_usuario.historial_pedido(session['user_id'])
        return render_template('historial_pedido.html', pedidos=pedidos)
    except Exception as e:
        flash(f'Error al cargar el historial de pedidos: {str(e)}', 'danger')
        return redirect(url_for('index'))

@app.route('/ver_detalle_pedido/<int:id>')
def ver_detalle_pedido(id):
    detalle = controlador_usuario.historial_detalle_pedido(id)
    print(detalle)
    return render_template('detalle_pedido.html', detalle=detalle)

@app.route('/login', methods=['POST'])
def login():
    usuario = request.form['usuario']
    contrasenia = request.form['contrasenia']
    user = controlador_usuario.login(usuario, contrasenia)
    if user:
        session['logged_in'] = True
        session['user_type'] = user[0][0]
        session['user_id'] = user[0][1]
        session['user_name'] = user[0][2]
        
        if session['user_type'] == 2:
            return jsonify({'success': True, 'redirect_url': url_for('admin_home')})
        else:
            return jsonify({'success': True, 'redirect_url': url_for('index')})
    else:
        return jsonify({'success': False, 'message': 'Usuario o contraseña incorrectos'})

@app.route('/logout')
def logout():
    session.clear()
    flash('Has cerrado sesión exitosamente.')
    return redirect(url_for('index'))

    













if __name__ == '__main__':
    app.run(debug=True)
