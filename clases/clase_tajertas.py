class clsTajetas: 
    id = 0
    numero_tarjeta = ""
    nombre_titular = ""
    fecha_expiracion = ""
    codigo_seguridad = ""
    usuario_id = 0
    dictajeta = dict()
    
    def __init__(self, p_id, p_numero_tarjeta, p_nombre_titular, p_fecha_expiracion, p_codigo_seguridad, p_usuario_id):
        self.id = p_id
        self.numero_tarjeta = p_numero_tarjeta
        self.nombre_titular = p_nombre_titular
        self.fecha_expiracion = p_fecha_expiracion
        self.codigo_seguridad = p_codigo_seguridad
        self.usuario_id = p_usuario_id
        
        self.dictajeta["id"] = p_id
        self.dictajeta["numero_tarjeta"] = p_numero_tarjeta
        self.dictajeta["nombre_titular"] = p_nombre_titular
        self.dictajeta["fecha_expiracion"] = p_fecha_expiracion
        self.dictajeta["codigo_seguridad"] = p_codigo_seguridad
        self.dictajeta["usuario_id"] = p_usuario_id
