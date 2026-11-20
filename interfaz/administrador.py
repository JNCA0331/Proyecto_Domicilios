import flet as ft
from modelos.usuario import Restaurante, Domiciliario
from logica.autenticacion import MediadorAutenticacion

class AdministradorUI:

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

        self.contenido = ft.Container(
            expand=True,
            padding=30
        )
        self.mediador = MediadorAutenticacion()
    #restaurantes
        self.nombre_restaurante = ft.TextField(
            label="Nombre del restaurante",
            width=300
        )

        self.usuario_restaurante = ft.TextField(
            label="Nombre de usuario",
            width=300
        )

        self.contrasena_restaurante = ft.TextField(
            label="Contraseña",
            password=True,
            can_reveal_password=True,
            width=300
        )

        self.mensaje_restaurante = ft.Text("")
        #domiciliarios
        self.nombre_domiciliario = ft.TextField(
            label="Nombre del domiciliario",
            width=300
        )

        self.usuario_domiciliario = ft.TextField(
            label="Nombre de usuario",
            width=300
        )

        self.contrasena_domiciliario = ft.TextField(
            label="Contraseña",
            password=True,
            can_reveal_password=True,
            width=300
        )

        self.mensaje_domiciliario = ft.Text("")

    def mostrar(self):

        barra_lateral = ft.Container(
            width=250,
            bgcolor=self.MORADO,
            padding=20,
            content=ft.Column(
                [
                    ft.Text(
                        "DOMICILIOS",
                        size=23,
                        weight=ft.FontWeight.BOLD,
                        color=self.BLANCO
                    ),

                    ft.Divider(color="#FFFFFF55"),

                    self.crear_boton("Inicio", self.mostrar_inicio),
                    self.crear_boton("Restaurantes", self.mostrar_restaurantes),
                    self.crear_boton("Domiciliarios", self.mostrar_domiciliarios),
                    self.crear_boton("Solicitudes", self.mostrar_solicitudes),
                    self.crear_boton("Finanzas", self.mostrar_finanzas),

                    ft.Container(expand=True),

                    ft.Button(
                        "Cerrar sesión",
                        icon=ft.Icons.LOGOUT,
                        color=self.BLANCO,
                        bgcolor=self.VERDE,
                        on_click=self.cerrar_sesion
                    )
                ],
                spacing=15
            )
        )

        self.page.controls.clear()

        self.page.add(
            ft.Row(
                [
                    barra_lateral,
                    self.contenido
                ],
                expand=True,
                spacing=0
            )
        )

        self.mostrar_inicio()
        self.page.update()

    def crear_boton(self, texto, funcion):

        return ft.Button(
            texto,
            width=210,
            color=self.BLANCO,
            bgcolor="#A64B80",
            on_click=funcion
        )

    def mostrar_inicio(self):

        self.contenido.content = ft.Column(
            [
                ft.Text(
                    "Panel de administración",
                    size=30,
                    weight=ft.FontWeight.BOLD,
                    color=self.MORADO
                ),

                ft.Text(
                    f"Bienvenido, {self.usuario.nombre}",
                    size=18,
                    color=self.NEGRO
                ),

                ft.Row(
                    [
                        self.crear_tarjeta("Restaurantes", "Gestionar cuentas"),
                        self.crear_tarjeta("Domiciliarios", "Gestionar cuentas")
                    ],
                    spacing=20
                ),

                ft.Row(
                    [
                        self.crear_tarjeta("Solicitudes", "Consultar entregas"),
                        self.crear_tarjeta("Finanzas", "Pagos y comisiones")
                    ],
                    spacing=20
                )
            ],
            spacing=25
        )

        self.page.update()

    def crear_tarjeta(self, titulo, descripcion):

        return ft.Container(
            expand=True,
            height=150,
            bgcolor=self.BLANCO,
            border_radius=20,
            padding=20,
            shadow=ft.BoxShadow(
                blur_radius=10,
                color="#00000015"
            ),
            content=ft.Column(
                [
                    ft.Text(
                        titulo,
                        size=20,
                        weight=ft.FontWeight.BOLD,
                        color=self.MORADO
                    ),
                    ft.Text(
                        descripcion,
                        color="#666666"
                    )
                ],
                spacing=10
            )
        )

    def mostrar_restaurantes(self):

        restaurantes = self.mediador.listar_usuarios("restaurante")

        lista = ft.Column(spacing=10)

        for restaurante in restaurantes:
            lista.controls.append(
                ft.Container(
                    bgcolor=self.BLANCO,
                    padding=15,
                    border_radius=15,
                    content=ft.Row(
                        [
                            ft.Column(
                                [
                                    ft.Text(
                                        restaurante[1],
                                        weight=ft.FontWeight.BOLD,
                                        color=self.MORADO
                                    ),
                                    ft.Text(
                                        "Usuario: " + restaurante[2],
                                        color="#666666"
                                    )
                                ],
                                expand=True
                            ),
                            ft.Icon(
                                ft.Icons.STORE,
                                color=self.VERDE
                            )
                        ]
                    )
                )
            )

        self.contenido.content = ft.Column(
            [
                ft.Text(
                    "Gestión de restaurantes",
                    size=30,
                    weight=ft.FontWeight.BOLD,
                    color=self.MORADO
                ),

                ft.Text("Registrar nuevo restaurante", size=20),

                self.nombre_restaurante,
                self.usuario_restaurante,
                self.contrasena_restaurante,

                ft.Button(
                    "Registrar restaurante",
                    icon=ft.Icons.ADD,
                    bgcolor=self.VERDE,
                    color=self.BLANCO,
                    on_click=self.registrar_restaurante
                ),

                self.mensaje_restaurante,

                ft.Divider(),

                ft.Text(
                    "Restaurantes registrados",
                    size=20,
                    weight=ft.FontWeight.BOLD
                ),

                lista
            ],
            scroll=ft.ScrollMode.AUTO,
            spacing=15
        )

        self.page.update()

    def registrar_restaurante(self, e):

        nombre = self.nombre_restaurante.value.strip()
        usuario = self.usuario_restaurante.value.strip()
        contrasena = self.contrasena_restaurante.value

        if not nombre or not usuario or not contrasena:
            self.mensaje_restaurante.value = "Completa todos los campos"
            self.page.update()
            return

        nuevo_restaurante = Restaurante(nombre, usuario)

        try:

            self.mediador.registrar_usuario(
                nuevo_restaurante,
                contrasena,
                self.usuario
            )

            self.nombre_restaurante.value = ""
            self.usuario_restaurante.value = ""
            self.contrasena_restaurante.value = ""

            self.mensaje_restaurante.value = "Restaurante registrado correctamente"

            self.mostrar_restaurantes()

        except Exception as error:

            self.mensaje_restaurante.value = "No se pudo registrar: " + str(error)
            self.page.update()

    def mostrar_domiciliarios(self):

        domiciliarios = self.mediador.listar_usuarios("domiciliario")

        lista = ft.Column(spacing=10)

        for domiciliario in domiciliarios:
            lista.controls.append(
                ft.Container(
                    bgcolor=self.BLANCO,
                    padding=15,
                    border_radius=15,
                    content=ft.Row(
                        [
                            ft.Column(
                                [
                                    ft.Text(
                                        domiciliario[1],
                                        weight=ft.FontWeight.BOLD,
                                        color=self.MORADO
                                    ),
                                    ft.Text(
                                        "Usuario: " + domiciliario[2],
                                        color="#666666"
                                    )
                                ],
                                expand=True
                            ),
                            ft.Icon(
                                ft.Icons.MOTORCYCLE,
                                color=self.VERDE
                            )
                        ]
                    )
                )
            )

        self.contenido.content = ft.Column(
            [
                ft.Text(
                    "Gestión de domiciliarios",
                    size=30,
                    weight=ft.FontWeight.BOLD,
                    color=self.MORADO
                ),

                ft.Text(
                    "Registrar nuevo domiciliario",
                    size=20
                ),

                self.nombre_domiciliario,
                self.usuario_domiciliario,
                self.contrasena_domiciliario,

                ft.Button(
                    "Registrar domiciliario",
                    icon=ft.Icons.ADD,
                    bgcolor=self.VERDE,
                    color=self.BLANCO,
                    on_click=self.registrar_domiciliario
                ),

                self.mensaje_domiciliario,

                ft.Divider(),

                ft.Text(
                    "Domiciliarios registrados",
                    size=20,
                    weight=ft.FontWeight.BOLD
                ),

                lista
            ],
            scroll=ft.ScrollMode.AUTO,
            spacing=15
        )

        self.page.update()

    def registrar_domiciliario(self, e):

        nombre = self.nombre_domiciliario.value.strip()
        usuario = self.usuario_domiciliario.value.strip()
        contrasena = self.contrasena_domiciliario.value

        if not nombre or not usuario or not contrasena:
            self.mensaje_domiciliario.value = "Completa todos los campos"
            self.page.update()
            return

        nuevo_domiciliario = Domiciliario(nombre, usuario)

        try:

            self.mediador.registrar_usuario(
                nuevo_domiciliario,
                contrasena,
                self.usuario
            )

            self.nombre_domiciliario.value = ""
            self.usuario_domiciliario.value = ""
            self.contrasena_domiciliario.value = ""

            self.mensaje_domiciliario.value = (
                "Domiciliario registrado correctamente"
            )

            self.mostrar_domiciliarios()

        except Exception as error:

            self.mensaje_domiciliario.value = (
                    "No se pudo registrar: " + str(error)
            )

            self.page.update()

    def mostrar_solicitudes(self):

        solicitudes = self.mediador.listar_solicitudes()

        elementos = []

        for solicitud in solicitudes:
            elementos.append(
                ft.Container(
                    bgcolor=self.BLANCO,
                    padding=18,
                    border_radius=15,
                    content=ft.Column(
                        [
                            ft.Row(
                                [
                                    ft.Text(
                                        f"Solicitud #{solicitud[0]}",
                                        weight=ft.FontWeight.BOLD,
                                        color=self.MORADO
                                    ),
                                    ft.Text(
                                        solicitud[5],
                                        color=self.VERDE
                                    )
                                ],
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                            ),

                            ft.Text("Restaurante: " + solicitud[1]),
                            ft.Text("Destinatario: " + solicitud[2]),
                            ft.Text("Dirección: " + solicitud[3]),
                            ft.Text(f"Tarifa: ${solicitud[4]:,.0f} COP"),
                            ft.Text(
                                "Domiciliario: " +
                                (solicitud[6] or "Sin asignar")
                            ),
                            ft.Text(
                                "Fecha: " + solicitud[7],
                                size=12,
                                color="#777777"
                            )
                        ],
                        spacing=7
                    )
                )
            )

        if not elementos:
            elementos.append(
                ft.Text(
                    "Todavía no hay solicitudes registradas.",
                    color="#777777"
                )
            )

        self.contenido.content = ft.Column(
            [
                ft.Text(
                    "Gestión de solicitudes",
                    size=30,
                    weight=ft.FontWeight.BOLD,
                    color=self.MORADO
                ),

                ft.Text(
                    "Consulta y seguimiento de los domicilios.",
                    color="#666666"
                ),

                *elementos
            ],
            scroll=ft.ScrollMode.AUTO,
            spacing=15
        )

        self.page.update()

    def mostrar_finanzas(self):

        pagos = self.mediador.listar_pagos()

        porcentaje = self.mediador.obtener_porcentaje_comision()

        total = sum(pago[4] for pago in pagos)
        comisiones = sum(pago[6] for pago in pagos)
        domiciliarios = sum(pago[7] for pago in pagos)

        elementos = []

        for pago in pagos:
            elementos.append(
                ft.Container(
                    bgcolor=self.BLANCO,
                    padding=18,
                    border_radius=15,
                    content=ft.Column(
                        [
                            ft.Text(
                                f"Pago #{pago[0]} - Solicitud #{pago[1]}",
                                weight=ft.FontWeight.BOLD,
                                color=self.MORADO
                            ),

                            ft.Text("Restaurante: " + pago[2]),
                            ft.Text("Domiciliario: " + pago[3]),
                            ft.Text(f"Valor: ${pago[4]:,.0f} COP"),
                            ft.Text(
                                f"Comisión ({pago[5]}%): "
                                f"${pago[6]:,.0f} COP"
                            ),
                            ft.Text(
                                f"Valor domiciliario: "
                                f"${pago[7]:,.0f} COP"
                            ),
                            ft.Text("Estado: " + pago[8]),
                            ft.Text(
                                "Fecha: " + pago[9],
                                size=12,
                                color="#777777"
                            )
                        ],
                        spacing=7
                    )
                )
            )

        if not elementos:
            elementos.append(
                ft.Text(
                    "Todavía no hay pagos registrados.",
                    color="#777777"
                )
            )

        self.comision_input = ft.TextField(
            label="Porcentaje de comisión",
            value=str(porcentaje),
            width=220
        )

        self.mensaje_finanzas = ft.Text("")

        self.contenido.content = ft.Column(
            [
                ft.Text(
                    "Gestión financiera",
                    size=30,
                    weight=ft.FontWeight.BOLD,
                    color=self.MORADO
                ),

                ft.Text(
                    "Resumen de pagos registrados",
                    size=20,
                    weight=ft.FontWeight.BOLD
                ),

                ft.Row(
                    [
                        self.crear_tarjeta(
                            "Total registrado",
                            f"${total:,.0f} COP"
                        ),

                        self.crear_tarjeta(
                            "Comisiones",
                            f"${comisiones:,.0f} COP"
                        ),

                        self.crear_tarjeta(
                            "Domiciliarios",
                            f"${domiciliarios:,.0f} COP"
                        )
                    ],
                    spacing=15
                ),

                ft.Divider(),

                ft.Text(
                    "Configuración de comisión",
                    size=20,
                    weight=ft.FontWeight.BOLD
                ),

                self.comision_input,

                ft.Text(
                    "La comisión debe estar entre 10% y 20%.",
                    size=12,
                    color="#777777"
                ),

                ft.Button(
                    "Guardar comisión",
                    icon=ft.Icons.SAVE,
                    bgcolor=self.VERDE,
                    color=self.BLANCO,
                    on_click=self.guardar_comision
                ),

                self.mensaje_finanzas,

                ft.Divider(),

                ft.Text(
                    "Historial de pagos",
                    size=20,
                    weight=ft.FontWeight.BOLD
                ),

                *elementos
            ],
            scroll=ft.ScrollMode.AUTO,
            spacing=15
        )

        self.page.update()

    def guardar_comision(self, e):

        try:

            porcentaje = float(self.comision_input.value)

            self.mediador.actualizar_porcentaje_comision(
                porcentaje
            )

            self.mensaje_finanzas.value = (
                "Comisión actualizada correctamente"
            )

            self.page.update()

        except ValueError as error:

            self.mensaje_finanzas.value = str(error)
            self.page.update()

    def mostrar_seccion(self, titulo):

        self.contenido.content = ft.Column(
            [
                ft.Text(
                    titulo,
                    size=30,
                    weight=ft.FontWeight.BOLD,
                    color=self.MORADO
                ),
                ft.Text(
                    "Este módulo estará disponible próximamente.",
                    size=16
                )
            ],
            spacing=20
        )

        self.page.update()

    def cerrar_sesion(self, e):

        from interfaz.login import Login

        login = Login(self.page)
        login.mostrar()
