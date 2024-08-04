class clsPago:
    id = 0
    pedido_id = 0
    tarjeta_id = 0
    fecha_pago = ""
    monto = 0.0
    estado = ""
    dicpago = dict()
    
    def __init__(self, p_id, p_pedido_id, p_tarjeta_id, p_fecha_pago, p_monto, p_estado):
        self.id = p_id
        self.pedido_id = p_pedido_id
        self.tarjeta_id = p_tarjeta_id
        self.fecha_pago = p_fecha_pago
        self.monto = p_monto
        self.estado = p_estado
        
        self.dicpago["id"] = p_id
        self.dicpago["pedido_id"] = p_pedido_id
        self.dicpago["tarjeta_id"] = p_tarjeta_id
        self.dicpago["fecha_pago"] = p_fecha_pago
        self.dicpago["monto"] = p_monto
        self.dicpago["estado"] = p_estado