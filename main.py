import flet as ft
from interfaz.login import Login

def main(page: ft.Page):

    page.title = "Plataforma de Domicilios"
    page.bgcolor = "#CFFFE2"

    page.window.maximized = True

    page.padding = 0
    page.spacing = 0

    page.theme_mode = ft.ThemeMode.LIGHT

    login = Login(page)
    login.mostrar()

ft.run(main)
