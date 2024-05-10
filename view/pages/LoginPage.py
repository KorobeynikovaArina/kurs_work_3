import flet as ft

from services.UserService import UserService
from view.ROUTES import HOME


def login_page(page: ft.Page):
    userService = UserService()

    er = ft.Text(value="", color="red")

    def login(e):
        if username.value == "" or password.value == "":
            return
        token = userService.login(username.value, password.value)
        if not token:
            er.value = "Wrong username or password"
            page.update()
            return
        page.client_storage.set("token", token)
        page.go(HOME)

    username = ft.TextField(hint_text="Username", autofocus=True)
    password = ft.TextField(hint_text="Password",
                            password=True, on_submit=login)
    submit = ft.TextButton(text="Login", on_click=login)
    return [
        ft.ResponsiveRow([
            ft.Container(col={"sm": 4},
                         content=ft.Column([username, password, submit, er]))],
                         alignment=ft.MainAxisAlignment.CENTER)
    ]
