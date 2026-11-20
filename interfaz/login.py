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
                        )
                    )
            )