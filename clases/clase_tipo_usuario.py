class clsTipoUser:
    id = 0
    nombre = ""
    diccateogoria = dict()

    def __init__(self, p_id, p_nombre):
        self.id = p_id
        self.nombre = p_nombre
        
        
        self.diccateogoria["id"] = p_id
        self.diccateogoria["nombre"] = p_nombre
        
