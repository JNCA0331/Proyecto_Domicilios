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
        self.crear_tablas_operacion()

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

    def listar_usuarios(self, rol):

        conexion = self.conectar()
        cursor = conexion.cursor()

        try:
            cursor.execute("""
                           SELECT id, nombre, usuario, rol
                           FROM usuarios
                           WHERE rol = ?
                           """, (rol,))

            return cursor.fetchall()

        finally:
            conexion.close()

    def crear_tablas_operacion(self):

        conexion = self.conectar()
        cursor = conexion.cursor()

        cursor.execute("""
                       CREATE TABLE IF NOT EXISTS solicitudes
                       (
                           id
                           INTEGER
                           PRIMARY
                           KEY
                           AUTOINCREMENT,
                           restaurante
                           TEXT
                           NOT
                           NULL,
                           destinatario
                           TEXT
                           NOT
                           NULL,
                           telefono
                           TEXT
                           NOT
                           NULL,
                           direccion
                           TEXT
                           NOT
                           NULL,
                           instrucciones
                           TEXT,
                           tarifa
                           REAL
                           NOT
                           NULL,
                           estado
                           TEXT
                           DEFAULT
                           'Generada',
                           domiciliario
                           TEXT,
                           fecha
                           TEXT
                           DEFAULT
                           CURRENT_TIMESTAMP
                       )
                       """)

        cursor.execute("""
                       CREATE TABLE IF NOT EXISTS pagos
                       (
                           id
                           INTEGER
                           PRIMARY
                           KEY
                           AUTOINCREMENT,
                           solicitud_id
                           INTEGER
                           NOT
                           NULL,
                           restaurante
                           TEXT
                           NOT
                           NULL,
                           domiciliario
                           TEXT
                           NOT
                           NULL,
                           monto_total
                           REAL
                           NOT
                           NULL,
                           porcentaje_comision
                           REAL
                           NOT
                           NULL,
                           comision
                           REAL
                           NOT
                           NULL,
                           monto_domiciliario
                           REAL
                           NOT
                           NULL,
                           estado
                           TEXT
                           DEFAULT
                           'Pendiente',
                           fecha
                           TEXT
                           DEFAULT
                           CURRENT_TIMESTAMP
                       )
                       """)

        cursor.execute("""
                       CREATE TABLE IF NOT EXISTS configuracion_financiera
                       (
                           id
                           INTEGER
                           PRIMARY
                           KEY,
                           porcentaje_comision
                           REAL
                           NOT
                           NULL
                       )
                       """)

        cursor.execute("""
                       INSERT
                       OR IGNORE INTO configuracion_financiera
            (id, porcentaje_comision)
            VALUES (1, 20)
                       """)

        conexion.commit()
        conexion.close()

    def listar_solicitudes(self):

        conexion = self.conectar()
        cursor = conexion.cursor()

        try:
            cursor.execute("""
                           SELECT id,
                                  restaurante,
                                  destinatario,
                                  direccion,
                                  tarifa,
                                  estado,
                                  domiciliario,
                                  fecha
                           FROM solicitudes
                           ORDER BY id DESC
                           """)

            return cursor.fetchall()

        finally:
            conexion.close()

    def listar_pagos(self):

        conexion = self.conectar()
        cursor = conexion.cursor()

        try:
            cursor.execute("""
                           SELECT id,
                                  solicitud_id,
                                  restaurante,
                                  domiciliario,
                                  monto_total,
                                  porcentaje_comision,
                                  comision,
                                  monto_domiciliario,
                                  estado,
                                  fecha
                           FROM pagos
                           ORDER BY id DESC
                           """)

            return cursor.fetchall()

        finally:
            conexion.close()

    def obtener_porcentaje_comision(self):

        conexion = self.conectar()
        cursor = conexion.cursor()

        try:
            cursor.execute("""
                           SELECT porcentaje_comision
                           FROM configuracion_financiera
                           WHERE id = 1
                           """)

            resultado = cursor.fetchone()

            return resultado[0] if resultado else 20

        finally:
            conexion.close()

    def actualizar_porcentaje_comision(self, porcentaje):

        porcentaje = float(porcentaje)

        if porcentaje < 10 or porcentaje > 20:
            raise ValueError(
                "La comisión debe estar entre 10% y 20%"
            )

        conexion = self.conectar()
        cursor = conexion.cursor()

        try:
            cursor.execute("""
                           UPDATE configuracion_financiera
                           SET porcentaje_comision = ?
                           WHERE id = 1
                           """, (porcentaje,))

            conexion.commit()

        finally:
            conexion.close()

    def registrar_solicitud(
            self, restaurante, destinatario, telefono,
            direccion, instrucciones, tarifa
    ):

        conexion = self.conectar()
        cursor = conexion.cursor()

        try:
            cursor.execute("""
                           INSERT INTO solicitudes
                           (restaurante, destinatario, telefono,
                            direccion, instrucciones, tarifa)
                           VALUES (?, ?, ?, ?, ?, ?)
                           """, (
                               restaurante, destinatario, telefono,
                               direccion, instrucciones, tarifa
                           ))

            conexion.commit()
            return cursor.lastrowid

        finally:
            conexion.close()

    def registrar_pago(
            self, solicitud_id, restaurante,
            domiciliario, monto_total
    ):

        monto_total = float(monto_total)
        porcentaje = self.obtener_porcentaje_comision()

        if monto_total <= 0:
            raise ValueError("El monto debe ser mayor que cero")

        comision = monto_total * porcentaje / 100
        monto_domiciliario = monto_total - comision

        conexion = self.conectar()
        cursor = conexion.cursor()

        try:
            cursor.execute("""
                           INSERT INTO pagos
                           (solicitud_id, restaurante, domiciliario,
                            monto_total, porcentaje_comision,
                            comision, monto_domiciliario)
                           VALUES (?, ?, ?, ?, ?, ?, ?)
                           """, (
                               solicitud_id, restaurante, domiciliario,
                               monto_total, porcentaje, comision,
                               monto_domiciliario
                           ))

            conexion.commit()

        finally:
            conexion.close()
