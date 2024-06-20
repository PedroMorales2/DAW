class clsProducto:
    id = 0
    nombre = ""
    descripcion = ""
    precio = 0
    stock = 0
    categoria_id = 0
    imagen = ""
    fecha_creacion = ""
    talla = ""
    genero = ""
    diccproducto = dict()

    def __init__(self, p_id, p_nombre, p_descripcion, p_precio, p_stock, p_categoria_id, p_imagen, p_fecha_creacion, p_talla, p_genero):
        self.id = p_id
        self.nombre = p_nombre
        self.descripcion = p_descripcion
        self.precio = p_precio
        self.stock = p_stock
        self.categoria_id = p_categoria_id
        self.imagen = p_imagen
        self.fecha_creacion = p_fecha_creacion
        self.tipo_usuario_id = p_talla
        self.genero = p_genero
        
        self.diccproducto["id"] = p_id
        self.diccproducto["nombre"] = p_nombre
        self.diccproducto["descripcion"] = p_descripcion
        self.diccproducto["precio"] = p_precio
        self.diccproducto["stock"] = p_stock
        self.diccproducto["categoria_id"] = p_categoria_id
        self.diccproducto["imagen"] = p_imagen
        self.diccproducto["fecha_creacion"] = p_fecha_creacion
        self.diccproducto["talla"] = p_talla
        self.diccproducto["genero"] = p_genero