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

