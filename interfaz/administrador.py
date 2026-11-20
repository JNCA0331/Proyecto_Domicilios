import flet as ft


class AdministradorUI:

    def __init__(self, page, usuario):

        self.page = page
        self.usuario = usuario

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
        self.mostrar_seccion("Gestión de restaurantes")

    def mostrar_domiciliarios(self):
        self.mostrar_seccion("Gestión de domiciliarios")

    def mostrar_solicitudes(self):
        self.mostrar_seccion("Gestión de solicitudes")

    def mostrar_finanzas(self):
        self.mostrar_seccion("Gestión financiera")

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
