import flet as ft
from logica.autenticacion import MediadorAutenticacion


class RestauranteUI:

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

        self.tarifa_seleccionada = 4000

        self.destinatario = ft.TextField(
            label="Nombre del destinatario",
            border_radius=15,
            border_color=self.MORADO,
            width=350
        )

        self.telefono = ft.TextField(
            label="Teléfono del destinatario",
            border_radius=15,
            border_color=self.MORADO,
            keyboard_type=ft.KeyboardType.PHONE,
            width=350
        )

        self.direccion = ft.TextField(
            label="Dirección de entrega",
            border_radius=15,
            border_color=self.MORADO,
            width=350
        )

        self.instrucciones = ft.TextField(
            label="Barrio o instrucciones adicionales",
            border_radius=15,
            border_color=self.MORADO,
            multiline=True,
            min_lines=2,
            max_lines=3,
            width=350
        )

        self.mensaje = ft.Text(
            "",
            color=self.MORADO,
            size=14
        )

        self.contenido = ft.Column(
            expand=True,
            scroll=ft.ScrollMode.AUTO
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
                        size=24,
                        weight=ft.FontWeight.BOLD,
                        color=self.MORADO
                    ),
                    ft.Container(expand=True),
                    ft.Button(
                        "Cerrar sesión",
                        icon=ft.Icons.LOGOUT,
                        bgcolor=self.MORADO,
                        color=self.BLANCO,
                        on_click=self.cerrar_sesion
                    )
                ]
            ),
            padding=20,
            bgcolor=self.BLANCO
        )

        menu = ft.Container(
            content=ft.Column(
                [
                    ft.Text(
                        "RESTAURANTE",
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
                        "Crear domicilio",
                        self.mostrar_crear_solicitud
                    ),

                    self.crear_boton(
                        "Mis solicitudes",
                        self.mostrar_solicitudes
                    )
                ],
                spacing=15
            ),
            bgcolor=self.MORADO,
            padding=20,
            width=240,
            expand=True
        )

        self.contenido.controls = [
            ft.Text(
                "Panel del restaurante",
                size=28,
                weight=ft.FontWeight.BOLD,
                color=self.MORADO
            ),
            ft.Text(
                "Administra tus solicitudes de domicilio.",
                size=16,
                color=self.NEGRO
            )
        ]

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

        self.contenido.controls = [
            ft.Text(
                "Inicio",
                size=28,
                weight=ft.FontWeight.BOLD,
                color=self.MORADO
            ),
            ft.Container(
                content=ft.Column(
                    [
                        ft.Icon(
                            ft.Icons.DELIVERY_DINING,
                            size=65,
                            color=self.VERDE
                        ),
                        ft.Text(
                            "¡Gestiona tus domicilios!",
                            size=22,
                            weight=ft.FontWeight.BOLD,
                            color=self.MORADO
                        ),
                        ft.Text(
                            "Desde este panel puedes solicitar "
                            "domiciliarios y consultar el estado "
                            "de tus entregas.",
                            size=16,
                            color=self.NEGRO,
                            text_align=ft.TextAlign.CENTER
                        ),
                        ft.Button(
                            "Crear una solicitud",
                            icon=ft.Icons.ADD,
                            bgcolor=self.VERDE,
                            color=self.BLANCO,
                            on_click=self.mostrar_crear_solicitud
                        )
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=15
                ),
                bgcolor=self.BLANCO,
                padding=35,
                border_radius=20,
                width=500
            )
        ]

        self.page.update()

    def seleccionar_tarifa(self, tarifa):

        self.tarifa_seleccionada = tarifa
        self.mensaje.value = (
            f"Tarifa seleccionada: ${tarifa:,.0f} COP"
        )
        self.page.update()

    def boton_tarifa(self, texto, tarifa):

        return ft.Button(
            texto,
            bgcolor=(
                self.VERDE
                if self.tarifa_seleccionada == tarifa
                else self.MORADO
            ),
            color=self.BLANCO,
            on_click=lambda e: self.seleccionar_tarifa(tarifa)
        )

    def mostrar_crear_solicitud(self):

        self.mensaje.value = ""

        self.contenido.controls = [
            ft.Text(
                "Crear solicitud de domicilio",
                size=27,
                weight=ft.FontWeight.BOLD,
                color=self.MORADO
            ),

            ft.Container(
                content=ft.Column(
                    [
                        self.destinatario,
                        self.telefono,
                        self.direccion,
                        self.instrucciones,

                        ft.Text(
                            "Selecciona la tarifa",
                            size=17,
                            weight=ft.FontWeight.BOLD,
                            color=self.MORADO
                        ),

                        ft.Row(
                            [
                                self.boton_tarifa(
                                    "$4.000",
                                    4000
                                ),
                                self.boton_tarifa(
                                    "$8.000",
                                    8000
                                ),
                                self.boton_tarifa(
                                    "$12.000",
                                    12000
                                )
                            ],
                            wrap=True
                        ),

                        self.mensaje,

                        ft.Button(
                            "Registrar domicilio",
                            icon=ft.Icons.SEND,
                            bgcolor=self.VERDE,
                            color=self.BLANCO,
                            on_click=self.registrar_solicitud
                        )
                    ],
                    spacing=15
                ),
                bgcolor=self.BLANCO,
                padding=25,
                border_radius=20,
                width=500
            )
        ]

        self.page.update()

    def registrar_solicitud(self, e):

        nombre = self.destinatario.value.strip()
        telefono = self.telefono.value.strip()
        direccion = self.direccion.value.strip()
        instrucciones = self.instrucciones.value.strip()

        if not nombre or not telefono or not direccion:
            self.mensaje.value = (
                "Completa el nombre, teléfono y dirección."
            )
            self.page.update()
            return

        try:

            self.mediador.registrar_solicitud(
                self.usuario.nombre,
                nombre,
                telefono,
                direccion,
                instrucciones,
                self.tarifa_seleccionada
            )

            self.mensaje.value = (
                "¡Solicitud registrada correctamente!"
            )
            self.mensaje.color = self.VERDE

            self.destinatario.value = ""
            self.telefono.value = ""
            self.direccion.value = ""
            self.instrucciones.value = ""

            self.page.update()

        except Exception as error:

            self.mensaje.value = f"Error al registrar: {error}"
            self.mensaje.color = self.MORADO
            self.page.update()

    def mostrar_solicitudes(self):

        solicitudes = self.mediador.listar_solicitudes()

        solicitudes_restaurante = [
            solicitud
            for solicitud in solicitudes
            if solicitud[1] == self.usuario.nombre
        ]

        controles = [
            ft.Text(
                "Mis solicitudes",
                size=27,
                weight=ft.FontWeight.BOLD,
                color=self.MORADO
            )
        ]

        if not solicitudes_restaurante:

            controles.append(
                ft.Text(
                    "Todavía no tienes solicitudes registradas.",
                    size=16,
                    color=self.NEGRO
                )
            )

        for solicitud in solicitudes_restaurante:

            (
                id_solicitud,
                restaurante,
                destinatario,
                direccion,
                tarifa,
                estado,
                domiciliario,
                fecha
            ) = solicitud

            controles.append(
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Text(
                                f"Solicitud #{id_solicitud}",
                                size=19,
                                weight=ft.FontWeight.BOLD,
                                color=self.MORADO
                            ),
                            ft.Text(
                                f"Destinatario: {destinatario}"
                            ),
                            ft.Text(
                                f"Dirección: {direccion}"
                            ),
                            ft.Text(
                                f"Tarifa: ${tarifa:,.0f} COP"
                            ),
                            ft.Text(
                                f"Estado: {estado}",
                                weight=ft.FontWeight.BOLD
                            ),
                            ft.Text(
                                f"Domiciliario: {domiciliario or 'Sin asignar'}"
                            ),
                            ft.Text(
                                f"Fecha: {fecha}",
                                size=12,
                                color="#64748B"
                            ),

                            ft.Text(
                                "Actualizar estado:",
                                weight=ft.FontWeight.BOLD,
                                color=self.MORADO
                            ),

                            ft.Row(
                                [
                                    ft.Button(
                                        "Recibida",
                                        bgcolor=self.VERDE,
                                        color=self.BLANCO,
                                        on_click=lambda e, sid=id_solicitud:
                                            self.actualizar_estado(
                                                sid, "Recibida"
                                            )
                                    ),
                                    ft.Button(
                                        "No recibida",
                                        bgcolor="#A66B20",
                                        color=self.BLANCO,
                                        on_click=lambda e, sid=id_solicitud:
                                            self.actualizar_estado(
                                                sid, "No recibida"
                                            )
                                    ),
                                    ft.Button(
                                        "Cancelar",
                                        bgcolor=self.MORADO,
                                        color=self.BLANCO,
                                        on_click=lambda e, sid=id_solicitud:
                                            self.actualizar_estado(
                                                sid, "Cancelada"
                                            )
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
                    width=650
                )
            )
        solicitudes = self.mediador.listar_solicitudes()

        print("USUARIO ACTUAL:", self.usuario.nombre)
        print("RESTAURANTES GUARDADOS:", [s[1] for s in solicitudes])

        self.contenido.controls = controles
        self.page.update()

    def actualizar_estado(self, id_solicitud, estado):

        try:

            self.mediador.actualizar_estado_solicitud(
                id_solicitud,
                self.usuario.nombre,
                estado
            )

            self.mostrar_solicitudes()

        except Exception as error:

            self.contenido.controls.append(
                ft.Text(
                    f"Error: {error}",
                    color=self.MORADO
                )
            )
            self.page.update()

    def cerrar_sesion(self, e):

        from interfaz.login import Login

        login = Login(self.page)
        login.mostrar()