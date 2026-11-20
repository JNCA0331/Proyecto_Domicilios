import sqlite3
import hashlib
import secrets
import hmac

from modelos.usuario import (
    Administrador,
    Restaurante,
    Domiciliario
)


class MediadorAutenticacion:

    def __init__(self):
        self.conexion = "usuarios.db"
        self.crear_tabla()
        self.crear_administrador_inicial()

    def conectar(self):
        return sqlite3.connect(self.conexion)

    def crear_tabla(self):

        conexion = self.conectar()
        cursor = conexion.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                usuario TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                salt TEXT NOT NULL,
                rol TEXT NOT NULL
            )
        """)

        conexion.commit()
        conexion.close()

    @staticmethod
    def generar_hash(contrasena, salt):

        return hashlib.pbkdf2_hmac(
            "sha256",
            contrasena.encode(),
            salt.encode(),
            200000
        ).hex()
    def crear_administrador_inicial(self):

        conexion = self.conectar()
        cursor = conexion.cursor()

        cursor.execute(
            "SELECT id FROM usuarios WHERE rol = ?",
            ("administrador",)
        )

        existe = cursor.fetchone()

        if not existe:

            salt = secrets.token_hex(16)

            password_hash = self.generar_hash(
                "Admin123*",
                salt
            )

            cursor.execute("""
                INSERT INTO usuarios
                (nombre, usuario, password_hash, salt, rol)
                VALUES (?, ?, ?, ?, ?)
            """, (
                "Administrador principal",
                "admin",
                password_hash,
                salt,
                "administrador"
            ))

        conexion.commit()
        conexion.close()

    def iniciar_sesion(self, usuario, contrasena):

        conexion = self.conectar()
        cursor = conexion.cursor()

        cursor.execute("""
            SELECT nombre, usuario, password_hash, salt, rol
            FROM usuarios
            WHERE usuario = ?
        """, (usuario,))

        resultado = cursor.fetchone()
        conexion.close()

        if resultado is None:
            return None

        nombre, usuario, password_hash, salt, rol = resultado

        hash_ingresado = self.generar_hash(
            contrasena,
            salt
        )

        if not hmac.compare_digest(
            password_hash,
            hash_ingresado
        ):
            return None

        clases = {
            "administrador": Administrador,
            "restaurante": Restaurante,
            "domiciliario": Domiciliario
        }

        clase_usuario = clases.get(rol)

        if clase_usuario is None:
            return None

        return clase_usuario(nombre, usuario)

    def registrar_usuario(self, usuario, contrasena, administrador):

        if not isinstance(administrador, Administrador):
            raise PermissionError(
                "Solo el administrador puede registrar usuarios"
            )

        if not contrasena:
            raise ValueError("La contraseña no puede estar vacía")

        rol = usuario.obtener_rol()

        if rol not in ("restaurante", "domiciliario"):
            raise ValueError("Tipo de usuario no permitido")

        salt = secrets.token_hex(16)

        password_hash = self.generar_hash(
            contrasena,
            salt
        )

        conexion = self.conectar()
        cursor = conexion.cursor()

        try:
            cursor.execute("""
                INSERT INTO usuarios
                (nombre, usuario, password_hash, salt, rol)
                VALUES (?, ?, ?, ?, ?)
            """, (
                usuario.nombre,
                usuario.usuario,
                password_hash,
                salt,
                rol
            ))

            conexion.commit()

        finally:
            conexion.close()
