from flet import *
import flet as ft

from services.UserService import UserService
from view.ROUTES import HOME


def login_page(page: ft.Page):
    page.title = 'Login'
    userService = UserService()

    def login(e):
        if username.value == '' or password.value == '':
            return
        token = userService.login(username.value, password.value)
        if not token:
            # error login invalid username or password
            return
        page.client_storage.set("token", token)
        page.go(HOME)

    username = ft.TextField(hint_text='Username', autofocus=True)
    password = ft.TextField(hint_text='Password',
                            password=True, on_submit=login)
    submit = ft.TextButton(text='Login', on_click=login)
    return [
        ft.ResponsiveRow([
            ft.Container(col={"sm": 4},
                         content=ft.Column([username, password, submit])),
        ], alignment=ft.MainAxisAlignment.CENTER, )
    ]