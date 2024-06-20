class clsUsuario:
    id = 0
    nombre = ""
    email = ""
    telefono = ""
    apellido = ""
    nombredeusuario = ""
    contraseña = ""
    fechaNacimiento = ""
    fecha_creacion = ""
    tipo_usuario_id = 0
    diccusuario = dict()

    def __init__(self, p_id, p_nombre, p_email, p_telefono, p_apellido, p_nombredeusuario, p_contraseña, p_fechaNacimiento, p_fecha_creacion, p_tipo_usuario_id):
        self.id = p_id
        self.nombre = p_nombre
        self.email = p_email
        self.telefono = p_telefono
        self.apellido = p_apellido
        self.nombredeusuario = p_nombredeusuario
        self.contraseña = p_contraseña
        self.fechaNacimiento = p_fechaNacimiento
        self.fecha_creacion = p_fecha_creacion
        self.tipo_usuario_id = p_tipo_usuario_id
        
        self.diccusuario["id"] = p_id
        self.diccusuario["nombre"] = p_nombre
        self.diccusuario["email"] = p_email
        self.diccusuario["telefono"] = p_telefono
        self.diccusuario["apellido"] = p_apellido
        self.diccusuario["nombredeusuario"] = p_nombredeusuario
        self.diccusuario["contraseña"] = p_contraseña
        self.diccusuario["fechaNacimiento"] = p_fechaNacimiento
        self.diccusuario["fecha_creacion"] = p_fecha_creacion
        self.diccusuario["tipo_usuario_id"] = p_tipo_usuario_id
