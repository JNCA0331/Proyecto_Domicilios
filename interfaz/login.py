import flet as ft
class Login:
    def __init__(self, page):
        self.page = page
        self.MORADO = "#872A60"
        self.VERDE = "#2A8751"
        self.MENTA = "#CFFFE2"
        self.ROSA = "#FFCFEC"
        self.BLANCO = "#FFFFFF"
        self.NEGRO = "#000000"

        self.usuario = ft.TextField(
            label="Usuario",
            prefix_icon=ft.Icons.PERSON,
            border_radius=20,
            border_color=self.MORADO,
            focused_border_color=self.VERDE,
            bgcolor=self.BLANCO,
            width=350
        )

        self.contrasena = ft.TextField(
            label="Contraseña",
            prefix_icon=ft.Icons.LOCK,
            password=True,
            can_reveal_password=True,
            border_radius=20,
            border_color=self.MORADO,
            focused_border_color=self.VERDE,
            bgcolor=self.BLANCO,
            width=350
        )

        self.mensaje = ft.Text(
            "",
            color=self.MORADO,
            size=14
        )

    def mostrar(self):
        logo = ft.Container(
            content=ft.Icon(
                ft.Icons.DELIVERY_DINING,
                size=75,
                color=self.BLANCO
            ),
            bgcolor=self.MORADO,
            width=120,
            height=120,
            border_radius=35,
            alignment=ft.Alignment.CENTER
        )

        formulario = ft.Container(
            content=ft.Column(
                [
                    logo,

                    ft.Text(
                        "¡Bienvenido!",
                        size=34,
                        weight=ft.FontWeight.BOLD,
                        color=self.MORADO
                    ),

                    ft.Text(
                        "Ingresa a tu plataforma de domicilios",
                        size=15,
                        color="#666666"
                    ),

                    ft.Container(height=15),

                    self.usuario,

                    self.contrasena,

                    self.mensaje,

                    ft.Container(
                        content=ft.ElevatedButton(
                            content=ft.Text(
                                "INICIAR SESIÓN",
                                weight=ft.FontWeight.BOLD,
                                color=self.BLANCO
                            ),
                            bgcolor=self.VERDE,
                            width=350,
                            height=55,
                            style=ft.ButtonStyle(
                                shape=ft.RoundedRectangleBorder(
                                    radius=20
                                )
                            ),
                            on_click=self.iniciar_sesion
                        )
                    ),

                    ft.Text(
                        "Sistema de gestión de domicilios",
                        size=12,
                        color="#888888"
                    )
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=15,
                tight=True
            ),

            bgcolor=self.BLANCO,
            padding=45,
            border_radius=35,
            width=460,
            shadow=ft.BoxShadow(
                blur_radius=25,
                color="#00000015",
                offset=ft.Offset(0, 8)
            )
        )

        fondo = ft.Container(
            content=formulario,
            bgcolor=self.MENTA,
            expand=True,
            alignment=ft.Alignment.CENTER
        )

        self.page.controls.clear()
        self.page.add(fondo)
        self.page.update()
