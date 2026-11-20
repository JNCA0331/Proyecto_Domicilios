class Usuario:

    def __init__(self, nombre, usuario):
        self.nombre = nombre
        self.usuario = usuario

    def obtener_rol(self):
        return "usuario"

class Administrador(Usuario):

    def obtener_rol(self):
        return "administrador"


class Restaurante(Usuario):

    def obtener_rol(self):
        return "restaurante"


class Domiciliario(Usuario):

    def obtener_rol(self):
        return "domiciliario"

