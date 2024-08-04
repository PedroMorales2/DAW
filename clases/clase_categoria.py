class clsCategoria:
    id = 0
    nombre = ""
    descripcion = ""
    fecha_creacion = ""
    diccateogoria = dict()

    def __init__(self, p_id, p_nombre, p_descripcion, p_fecha_creacion):
        self.id = p_id
        self.nombre = p_nombre
        self.descripcion = p_descripcion
        self.fecha_creacion = p_fecha_creacion

        
        self.diccateogoria["id"] = p_id
        self.diccateogoria["nombre"] = p_nombre
        self.diccateogoria["descripcion"] = p_descripcion
        self.diccateogoria["fecha_creacion"] = p_fecha_creacion
