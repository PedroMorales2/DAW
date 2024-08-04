class clsDireccion:
    id = 0
    pais = ""
    departamento = ""
    ciudad = ""
    codigo_postal = ""
    direccion1 = ""
    direccion2 = ""
    usuarios_id = 0
    dicdireccion = dict()
    
    def __init__(self, p_id, p_pais, p_departamento, p_ciudad, p_codigo_postal, p_direccion1, p_direccion2, p_usuarios_id):
        self.id = p_id
        self.pais = p_pais
        self.departamento = p_departamento
        self.ciudad = p_ciudad
        self.codigo_postal = p_codigo_postal
        self.direccion1 = p_direccion1
        self.direccion2 = p_direccion2
        self.usuarios_id = p_usuarios_id
        
        self.dicdireccion["id"] = p_id
        self.dicdireccion["pais"] = p_pais
        self.dicdireccion["departamento"] = p_departamento
        self.dicdireccion["ciudad"] = p_ciudad
        self.dicdireccion["codigo_postal"] = p_codigo_postal
        self.dicdireccion["direccion1"] = p_direccion1
        self.dicdireccion["direccion2"] = p_direccion2
        self.dicdireccion["usuarios_id"] = p_usuarios_id