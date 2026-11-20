import flet as ft
from logica.autenticacion import MediadorAutenticacion

class DomiciliarioUI:

    def __init__(self, page, usuario):

        self.page = page
        self.usuario = usuario
        self.mediador = MediadorAutenticacion()

        self.MORADO = "#872A60"
        self.VERDE = "#2A8751"
        self.MENTA = "#CFFFE2"
        self.ROSA = "#FFCFEC"
        self.BLANCO = "#FFFFFF"
        self.NEGRO = "#000000"

        self.contenido = ft.Column(
            expand=True,
            scroll=ft.ScrollMode.AUTO
        )

        self.mensaje = ft.Text(
            "",
            color=self.MORADO
        )

    def mostrar(self):

        self.page.clean()
        self.page.bgcolor = self.MENTA
        self.page.padding = 0

        encabezado = ft.Container(
            content=ft.Row(
                [
                    ft.Text(
                        f"Bienvenido, {self.usuario.nombre}",
                        size=23,
                        weight=ft.FontWeight.BOLD,
                        color=self.MORADO
                    ),
                    ft.Container(expand=True),
                    ft.Button(
                        "Cerrar sesión",
                        bgcolor=self.MORADO,
                        color=self.BLANCO,
                        on_click=self.cerrar_sesion
                    )
                ]
            ),
            bgcolor=self.BLANCO,
            padding=20
        )

        menu = ft.Container(
            content=ft.Column(
                [
                    ft.Text(
                        "DOMICILIARIO",
                        size=20,
                        weight=ft.FontWeight.BOLD,
                        color=self.BLANCO
                    ),

                    ft.Divider(color=self.BLANCO),

                    self.crear_boton(
                        "Inicio",
                        self.mostrar_inicio
                    ),

                    self.crear_boton(
                        "Solicitudes",
                        self.mostrar_solicitudes
                    ),

                    self.crear_boton(
                        "Mis entregas",
                        self.mostrar_entregas
                    ),

                    self.crear_boton(
                        "Historial",
                        self.mostrar_historial
                    )
                ],
                spacing=15
            ),
            bgcolor=self.MORADO,
            padding=20,
            width=240,
            expand=True
        )

        cuerpo = ft.Row(
            [
                menu,
                ft.Container(
                    content=self.contenido,
                    expand=True,
                    padding=30
                )
            ],
            expand=True,
            spacing=0
        )

        self.page.add(
            ft.Column(
                [
                    encabezado,
                    cuerpo
                ],
                expand=True,
                spacing=0
            )
        )

        self.mostrar_inicio()

    def crear_boton(self, texto, funcion):

        return ft.Button(
            texto,
            width=200,
            bgcolor="#A64B80",
            color=self.BLANCO,
            on_click=funcion
        )

    def mostrar_inicio(self):

        activo = self.mediador.obtener_estado_disponibilidad(
            self.usuario.usuario
        )

        estado = "ACTIVO" if activo else "INACTIVO"

        color_estado = self.VERDE if activo else self.MORADO

        self.contenido.controls = [
            ft.Text(
                "Panel del domiciliario",
                size=28,
                weight=ft.FontWeight.BOLD,
                color=self.MORADO
            ),

            ft.Container(
                content=ft.Column(
                    [
                        ft.Text(
                            f"Estado actual: {estado}",
                            size=22,
                            weight=ft.FontWeight.BOLD,
                            color=color_estado
                        ),

                        ft.Text(
                            "Activa tu disponibilidad para "
                            "poder recibir solicitudes.",
                            size=16,
                            color=self.NEGRO
                        ),

                        ft.Button(
                            "Desactivar disponibilidad"
                            if activo
                            else "Activar disponibilidad",
                            bgcolor=self.MORADO if activo else self.VERDE,
                            color=self.BLANCO,
                            on_click=self.cambiar_disponibilidad
                        ),

                        ft.Button(
                            "Actualizar solicitudes",
                            bgcolor=self.MORADO,
                            color=self.BLANCO,
                            on_click=self.actualizar_sistema
                        ),

                        self.mensaje
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=18
                ),
                bgcolor=self.BLANCO,
                padding=30,
                border_radius=20,
                width=500
            )
        ]

        self.page.update()

    def cambiar_disponibilidad(self, e):

        usuario = self.usuario.usuario

        try:

            activo = self.mediador.obtener_estado_disponibilidad(
                usuario
            )

            if activo:
                self.mediador.desactivar_domiciliario(usuario)
                self.mensaje.value = "Disponibilidad desactivada"

            else:
                self.mediador.activar_domiciliario(usuario)
                self.mensaje.value = "¡Ya estás disponible!"

            self.mostrar_inicio()

        except Exception as error:

            self.mensaje.value = str(error)
            self.page.update()

    def actualizar_sistema(self, e):

        try:

            self.mediador.procesar_solicitudes_pendientes()
            self.mensaje.value = "Solicitudes actualizadas"

            self.mostrar_inicio()

        except Exception as error:

            self.mensaje.value = str(error)
            self.page.update()

    def mostrar_solicitudes(self):

        try:
            self.mediador.procesar_solicitudes_pendientes()

            solicitudes = (
                self.mediador.listar_asignaciones_domiciliario(
                    self.usuario.usuario
                )
            )
            print("USUARIO DOMICILIARIO:", self.usuario.usuario)
            print("ASIGNACIONES ENCONTRADAS:", solicitudes)
            controles = [
                ft.Text(
                    "Solicitudes asignadas",
                    size=27,
                    weight=ft.FontWeight.BOLD,
                    color=self.MORADO
                )
            ]

            pendientes = [
                solicitud for solicitud in solicitudes
                if solicitud[7] == "Pendiente"
            ]

            if not pendientes:
                controles.append(
                    ft.Text(
                        "No tienes solicitudes pendientes.",
                        color=self.NEGRO
                    )
                )

            for solicitud in pendientes:

                (
                    id_asignacion,
                    id_solicitud,
                    destinatario,
                    telefono,
                    direccion,
                    instrucciones,
                    tarifa,
                    estado,
                    fecha
                ) = solicitud

                controles.append(
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Text(
                                    f"Solicitud #{id_solicitud}",
                                    size=20,
                                    weight=ft.FontWeight.BOLD,
                                    color=self.MORADO
                                ),
                                ft.Text(f"Destinatario: {destinatario}"),
                                ft.Text(f"Teléfono: {telefono}"),
                                ft.Text(f"Dirección: {direccion}"),
                                ft.Text(
                                    f"Instrucciones: {instrucciones or 'Ninguna'}"
                                ),
                                ft.Text(f"Tarifa: ${tarifa:,.0f} COP"),
                                ft.Text(f"Estado: {estado}"),

                                ft.Row(
                                    [
                                        ft.Button(
                                            "Aceptar",
                                            bgcolor=self.VERDE,
                                            color=self.BLANCO,
                                            on_click=lambda e, sid=id_solicitud:
                                                self.responder(sid, True)
                                        ),
                                        ft.Button(
                                            "Rechazar",
                                            bgcolor=self.MORADO,
                                            color=self.BLANCO,
                                            on_click=lambda e, sid=id_solicitud:
                                                self.responder(sid, False)
                                        )
                                    ],
                                    wrap=True
                                )
                            ],
                            spacing=8
                        ),
                        bgcolor=self.BLANCO,
                        padding=20,
                        border_radius=18,
                        width=600
                    )
                )

            self.contenido.controls = controles
            self.page.update()

        except Exception as error:

            self.contenido.controls = [
                ft.Text(
                    f"Error al consultar solicitudes: {error}",
                    color=self.MORADO
                )
            ]
            self.page.update()

    def responder(self, solicitud_id, aceptar):

        try:

            resultado = self.mediador.responder_asignacion(
                solicitud_id,
                self.usuario.usuario,
                aceptar
            )

            if resultado:
                self.mensaje.value = "¡Solicitud aceptada!"
            else:
                self.mensaje.value = (
                    "Solicitud rechazada o asignación vencida."
                )

            self.mostrar_solicitudes()

        except Exception as error:

            self.mensaje.value = str(error)

            self.contenido.controls.append(self.mensaje)
            self.page.update()

    def mostrar_entregas(self):

        try:

            solicitudes = (
                self.mediador.listar_asignaciones_domiciliario(
                    self.usuario.usuario
                )
            )

            activas = [
                solicitud for solicitud in solicitudes
                if solicitud[7] in (
                    "Aceptada",
                    "En camino",
                    "Recogida"
                )
            ]

            controles = [
                ft.Text(
                    "Mis entregas",
                    size=27,
                    weight=ft.FontWeight.BOLD,
                    color=self.MORADO
                )
            ]

            if not activas:
                controles.append(
                    ft.Text("No tienes entregas activas.")
                )

            for solicitud in activas:

                (
                    id_asignacion,
                    id_solicitud,
                    destinatario,
                    telefono,
                    direccion,
                    instrucciones,
                    tarifa,
                    estado,
                    fecha
                ) = solicitud

                botones = []

                if estado == "Aceptada":
                    botones.append(
                        ft.Button(
                            "Iniciar recorrido",
                            bgcolor=self.VERDE,
                            color=self.BLANCO,
                            on_click=lambda e, sid=id_solicitud:
                                self.cambiar_estado_entrega(
                                    sid, "En camino"
                                )
                        )
                    )

                elif estado == "En camino":
                    botones.append(
                        ft.Button(
                            "Confirmar recogida",
                            bgcolor=self.VERDE,
                            color=self.BLANCO,
                            on_click=lambda e, sid=id_solicitud:
                                self.cambiar_estado_entrega(
                                    sid, "Recogida"
                                )
                        )
                    )

                elif estado == "Recogida":
                    botones.append(
                        ft.Button(
                            "Finalizar entrega",
                            bgcolor=self.VERDE,
                            color=self.BLANCO,
                            on_click=lambda e, sid=id_solicitud:
                                self.finalizar(sid)
                        )
                    )

                controles.append(
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Text(
                                    f"Solicitud #{id_solicitud}",
                                    size=20,
                                    weight=ft.FontWeight.BOLD,
                                    color=self.MORADO
                                ),
                                ft.Text(f"Destinatario: {destinatario}"),
                                ft.Text(f"Teléfono: {telefono}"),
                                ft.Text(f"Dirección: {direccion}"),
                                ft.Text(f"Estado: {estado}"),
                                ft.Row(botones, wrap=True)
                            ],
                            spacing=8
                        ),
                        bgcolor=self.BLANCO,
                        padding=20,
                        border_radius=18,
                        width=600
                    )
                )

            self.contenido.controls = controles
            self.page.update()

        except Exception as error:

            self.contenido.controls = [
                ft.Text(f"Error: {error}", color=self.MORADO)
            ]
            self.page.update()

    def cambiar_estado_entrega(self, solicitud_id, estado):

        try:

            self.mediador.actualizar_estado_entrega(
                solicitud_id,
                self.usuario.usuario,
                estado
            )

            self.mostrar_entregas()

        except Exception as error:

            self.contenido.controls.append(
                ft.Text(str(error), color=self.MORADO)
            )
            self.page.update()

    def finalizar(self, solicitud_id):

        try:

            self.mediador.finalizar_entrega(
                solicitud_id,
                self.usuario.usuario
            )

            self.mostrar_entregas()

        except Exception as error:

            self.contenido.controls.append(
                ft.Text(str(error), color=self.MORADO)
            )
            self.page.update()

    def mostrar_historial(self):

        historial = (
            self.mediador.listar_asignaciones_domiciliario(
                self.usuario.usuario,
                historial=True
            )
        )

        controles = [
            ft.Text(
                "Historial de solicitudes",
                size=27,
                weight=ft.FontWeight.BOLD,
                color=self.MORADO
            )
        ]

        if not historial:
            controles.append(
                ft.Text("Todavía no tienes registros en tu historial.")
            )

        for solicitud in historial:

            controles.append(
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Text(
                                f"Solicitud #{solicitud[1]}",
                                weight=ft.FontWeight.BOLD,
                                color=self.MORADO
                            ),
                            ft.Text(f"Destinatario: {solicitud[2]}"),
                            ft.Text(f"Dirección: {solicitud[4]}"),
                            ft.Text(f"Estado: {solicitud[7]}"),
                            ft.Text(f"Fecha: {solicitud[8]}")
                        ],
                        spacing=6
                    ),
                    bgcolor=self.BLANCO,
                    padding=18,
                    border_radius=15,
                    width=600
                )
            )

        self.contenido.controls = controles
        self.page.update()

    def cerrar_sesion(self, e):

        from interfaz.login import Login

        login = Login(self.page)
        login.mostrar()