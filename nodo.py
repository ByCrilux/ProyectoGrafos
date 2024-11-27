class Nodo:
    def __init__(self, id_cuenta, nombre_cuenta):
        self.id_cuenta = id_cuenta
        self.nombre_cuenta = nombre_cuenta
        self.transacciones = []  # Lista de tuplas (destino, monto)

