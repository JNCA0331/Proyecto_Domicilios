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
#Funciones de usuario administrador

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
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS estado_domiciliarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario TEXT UNIQUE NOT NULL,
                disponible INTEGER DEFAULT 0,
                fecha_activacion TEXT
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS asignaciones (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                solicitud_id INTEGER NOT NULL,
                domiciliario TEXT NOT NULL,
                estado TEXT DEFAULT 'Pendiente',
                fecha_asignacion TEXT DEFAULT CURRENT_TIMESTAMP,
                limite_aceptacion TEXT
            )
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

#Funciones de usuarios restaurantes

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

            solicitud_id = cursor.lastrowid
            conexion.commit()

        finally:
            conexion.close()

        print("SOLICITUD REGISTRADA:", solicitud_id)

        domiciliario = self.asignar_siguiente(solicitud_id)

        print("DOMICILIARIO ASIGNADO:", domiciliario)

        return solicitud_id

    def registrar_pago(self, solicitud_id, restaurante, domiciliario, monto_total):

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

    def actualizar_estado_solicitud(self, id_solicitud, restaurante, estado):

        estados_permitidos = (
            "Recibida",
            "No recibida",
            "Cancelada"
        )

        if estado not in estados_permitidos:
            raise ValueError("Estado no permitido")

        conexion = self.conectar()
        cursor = conexion.cursor()

        try:

            cursor.execute("""
                           UPDATE solicitudes
                           SET estado = ?
                           WHERE id = ?
                             AND restaurante = ?
                           """, (
                               estado,
                               id_solicitud,
                               restaurante
                           ))

            if cursor.rowcount == 0:
                raise ValueError("No se encontró la solicitud")

            conexion.commit()

        finally:
            conexion.close()

#Funciones de usuario domiciliario

    def activar_domiciliario(self, usuario):

        from datetime import datetime

        conexion = self.conectar()
        cursor = conexion.cursor()

        try:
            cursor.execute("""
                           INSERT INTO estado_domiciliarios
                               (usuario, disponible, fecha_activacion)
                           VALUES (?, 1, ?) ON CONFLICT(usuario)
                DO
                           UPDATE SET
                               disponible = 1,
                               fecha_activacion = excluded.fecha_activacion
                           """, (
                               usuario,
                               datetime.now().isoformat()
                           ))

            conexion.commit()

        finally:
            conexion.close()

        self.procesar_solicitudes_pendientes()

    def desactivar_domiciliario(self, usuario):

        conexion = self.conectar()
        cursor = conexion.cursor()

        try:
            cursor.execute("""
                           UPDATE estado_domiciliarios
                           SET disponible = 0
                           WHERE usuario = ?
                           """, (usuario,))

            conexion.commit()

        finally:
            conexion.close()

    def obtener_cola_domiciliarios(self):

        conexion = self.conectar()
        cursor = conexion.cursor()

        try:
            cursor.execute("""
                           SELECT usuario, fecha_activacion
                           FROM estado_domiciliarios
                           WHERE disponible = 1
                           ORDER BY fecha_activacion ASC
                           """)

            return cursor.fetchall()

        finally:
            conexion.close()

    def contar_entregas_activas(self, usuario):

        conexion = self.conectar()
        cursor = conexion.cursor()

        try:
            cursor.execute("""
                           SELECT COUNT(*)
                           FROM asignaciones
                           WHERE domiciliario = ?
                             AND estado IN ('Aceptada', 'En camino', 'Recogida')
                           """, (usuario,))

            resultado = cursor.fetchone()

            return resultado[0]

        finally:
            conexion.close()

    def asignar_siguiente(self, solicitud_id):

        from datetime import datetime, timedelta

        conexion = self.conectar()
        cursor = conexion.cursor()

        try:
            cursor.execute("""
                           SELECT usuario
                           FROM estado_domiciliarios
                           WHERE disponible = 1
                           ORDER BY fecha_activacion ASC
                           """)

            domiciliarios = cursor.fetchall()

            print("DOMICILIARIOS DISPONIBLES:", domiciliarios)
            print("SOLICITUD A ASIGNAR:", solicitud_id)

            for fila in domiciliarios:

                usuario = fila[0]

                # Contar entregas activas
                cursor.execute("""
                               SELECT COUNT(*)
                               FROM asignaciones
                               WHERE domiciliario = ?
                                 AND estado IN ('Aceptada', 'En camino', 'Recogida')
                               """, (usuario,))

                cantidad = cursor.fetchone()[0]

                # Contar ofertas pendientes
                cursor.execute("""
                               SELECT COUNT(*)
                               FROM asignaciones
                               WHERE domiciliario = ?
                                 AND estado = 'Pendiente'
                               """, (usuario,))

                pendientes = cursor.fetchone()[0]

                print("DOMICILIARIO:", usuario)
                print("ENTREGAS ACTIVAS:", cantidad)
                print("OFERTAS PENDIENTES:", pendientes)

                if cantidad < 2 and pendientes == 0:
                    fecha_limite = datetime.now() + timedelta(seconds=30)

                    # Crear asignación
                    cursor.execute("""
                                   INSERT INTO asignaciones
                                   (solicitud_id, domiciliario, estado,
                                    fecha_asignacion, limite_aceptacion)
                                   VALUES (?, ?, 'Pendiente', ?, ?)
                                   """, (
                                       solicitud_id,
                                       usuario,
                                       datetime.now(),
                                       fecha_limite
                                   ))

                    # Actualizar solicitud
                    cursor.execute("""
                                   UPDATE solicitudes
                                   SET estado       = 'Esperando aceptación',
                                       domiciliario = ?
                                   WHERE id = ?
                                   """, (usuario, solicitud_id))

                    conexion.commit()

                    print("ASIGNACIÓN CREADA PARA:", usuario)

                    return usuario

            # Si ningún domiciliario puede recibirla
            cursor.execute("""
                           UPDATE solicitudes
                           SET estado       = 'Pendiente de domiciliario',
                               domiciliario = NULL
                           WHERE id = ?
                           """, (solicitud_id,))

            conexion.commit()

            return None

        finally:
            conexion.close()

    def responder_asignacion(self, solicitud_id, usuario, aceptar):

        from datetime import datetime

        conexion = self.conectar()
        cursor = conexion.cursor()

        try:
            cursor.execute("""
                           SELECT id, limite_aceptacion
                           FROM asignaciones
                           WHERE solicitud_id = ?
                             AND domiciliario = ?
                             AND estado = 'Pendiente'
                           ORDER BY id DESC LIMIT 1
                           """, (solicitud_id, usuario))

            asignacion = cursor.fetchone()

            if asignacion is None:
                raise ValueError("No tienes una asignación pendiente")

            id_asignacion, limite = asignacion

            if datetime.now() > datetime.fromisoformat(limite):
                cursor.execute("""
                               UPDATE asignaciones
                               SET estado = 'Vencida'
                               WHERE id = ?
                               """, (id_asignacion,))

                cursor.execute("""
                               UPDATE estado_domiciliarios
                               SET fecha_activacion = ?
                               WHERE usuario = ?
                               """, (datetime.now().isoformat(), usuario))

                conexion.commit()
                conexion.close()

                self.asignar_siguiente(solicitud_id)

                return False

            if aceptar:

                cursor.execute("""
                               SELECT COUNT(*)
                               FROM asignaciones
                               WHERE domiciliario = ?
                                 AND estado IN ('Aceptada', 'En camino', 'Recogida')
                               """, (usuario,))

                if cursor.fetchone()[0] >= 2:
                    raise ValueError("Ya tienes dos entregas activas")

                cursor.execute("""
                               UPDATE asignaciones
                               SET estado = 'Aceptada'
                               WHERE id = ?
                               """, (id_asignacion,))

                cursor.execute("""
                               UPDATE solicitudes
                               SET estado = 'Domiciliario asignado'
                               WHERE id = ?
                               """, (solicitud_id,))

                conexion.commit()
                return True

            else:

                cursor.execute("""
                               UPDATE asignaciones
                               SET estado = 'Rechazada'
                               WHERE id = ?
                               """, (id_asignacion,))

                cursor.execute("""
                               UPDATE estado_domiciliarios
                               SET fecha_activacion = ?
                               WHERE usuario = ?
                               """, (datetime.now().isoformat(), usuario))

                conexion.commit()

            conexion.close()

            self.asignar_siguiente(solicitud_id)

            return False

        finally:
            try:
                conexion.close()
            except Exception:
                pass

    def procesar_solicitudes_pendientes(self):

        from datetime import datetime

        conexion = self.conectar()
        cursor = conexion.cursor()

        try:
            ahora = datetime.now()

            cursor.execute("""
                           SELECT id, solicitud_id, domiciliario
                           FROM asignaciones
                           WHERE estado = 'Pendiente'
                           """)

            pendientes = cursor.fetchall()

            for id_asignacion, solicitud_id, usuario in pendientes:

                cursor.execute("""
                               SELECT limite_aceptacion
                               FROM asignaciones
                               WHERE id = ?
                               """, (id_asignacion,))

                limite = cursor.fetchone()[0]

                if ahora > datetime.fromisoformat(limite):
                    cursor.execute("""
                                   UPDATE asignaciones
                                   SET estado = 'Vencida'
                                   WHERE id = ?
                                   """, (id_asignacion,))

                    cursor.execute("""
                                   UPDATE estado_domiciliarios
                                   SET fecha_activacion = ?
                                   WHERE usuario = ?
                                   """, (ahora.isoformat(), usuario))

                    conexion.commit()

                    conexion.close()

                    self.asignar_siguiente(solicitud_id)

                    return self.procesar_solicitudes_pendientes()

            cursor.execute("""
                           SELECT id
                           FROM solicitudes
                           WHERE estado = 'Pendiente de domiciliario'
                           """)

            solicitudes = cursor.fetchall()

        finally:
            conexion.close()

        for solicitud in solicitudes:
            self.asignar_siguiente(solicitud[0])

    def finalizar_entrega(self, solicitud_id, usuario):

        from datetime import datetime

        conexion = self.conectar()
        cursor = conexion.cursor()

        try:
            cursor.execute("""
                           UPDATE asignaciones
                           SET estado = 'Entregada'
                           WHERE solicitud_id = ?
                             AND domiciliario = ?
                             AND estado IN ('Aceptada', 'En camino', 'Recogida')
                           """, (solicitud_id, usuario))

            if cursor.rowcount == 0:
                raise ValueError("No se encontró una entrega activa")

            cursor.execute("""
                           UPDATE solicitudes
                           SET estado = 'Entregada'
                           WHERE id = ?
                             AND domiciliario = ?
                           """, (solicitud_id, usuario))

            cursor.execute("""
                           UPDATE estado_domiciliarios
                           SET fecha_activacion = ?
                           WHERE usuario = ?
                             AND disponible = 1
                           """, (datetime.now().isoformat(), usuario))

            conexion.commit()

        finally:
            conexion.close()

        self.procesar_solicitudes_pendientes()

    #Funciones interfaz usuario
    def obtener_estado_disponibilidad(self, usuario):

        conexion = self.conectar()
        cursor = conexion.cursor()

        try:
            cursor.execute("""
                           SELECT disponible
                           FROM estado_domiciliarios
                           WHERE usuario = ?
                           """, (usuario,))

            resultado = cursor.fetchone()

            return bool(resultado[0]) if resultado else False

        finally:
            conexion.close()

    def listar_asignaciones_domiciliario(self, usuario, historial=False):

        conexion = self.conectar()
        cursor = conexion.cursor()

        try:

            if historial:
                estados = ("Rechazada", "Vencida", "Entregada")
            else:
                estados = (
                    "Pendiente",
                    "Aceptada",
                    "En camino",
                    "Recogida"
                )

            marcadores = ",".join("?" for _ in estados)

            cursor.execute(f"""
                SELECT
                    a.id,
                    a.solicitud_id,
                    s.destinatario,
                    s.telefono,
                    s.direccion,
                    s.instrucciones,
                    s.tarifa,
                    a.estado,
                    a.fecha_asignacion
                FROM asignaciones a
                INNER JOIN solicitudes s
                    ON a.solicitud_id = s.id
                WHERE a.domiciliario = ?
                AND a.estado IN ({marcadores})
                ORDER BY a.id DESC
            """, (usuario, *estados))

            return cursor.fetchall()

        finally:
            conexion.close()

    def actualizar_estado_entrega(self, solicitud_id, usuario, estado):

        estados_permitidos = ("En camino", "Recogida")

        if estado not in estados_permitidos:
            raise ValueError("Estado de entrega no permitido")

        conexion = self.conectar()
        cursor = conexion.cursor()

        try:

            cursor.execute("""
                           UPDATE asignaciones
                           SET estado = ?
                           WHERE solicitud_id = ?
                             AND domiciliario = ?
                             AND estado IN ('Aceptada', 'En camino', 'Recogida')
                           """, (estado, solicitud_id, usuario))

            if cursor.rowcount == 0:
                raise ValueError("No se encontró una entrega activa")

            cursor.execute("""
                           UPDATE solicitudes
                           SET estado = ?
                           WHERE id = ?
                             AND domiciliario = ?
                           """, (estado, solicitud_id, usuario))

            conexion.commit()

        finally:
            conexion.close()

