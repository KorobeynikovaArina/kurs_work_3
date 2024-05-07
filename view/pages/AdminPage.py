from flet import *
import flet as ft

from services.OrderService import OrderService
from services.UserService import UserService
from view.ROUTES import ADMIN_USERS, HOME, LOGIN, ADMIN_STATUS, ADMIN_CLIENTTYPE


def admin_page(page: ft.Page):
    userService = UserService()

    def logout(e):
        token = page.client_storage.get('token')
        userService.logout(token)
        page.client_storage.remove('token')

        page.go(LOGIN)

    logoutbtn = ft.TextButton(text='Logout', on_click=logout)
    homebtn = ft.TextButton(
        text="Home", on_click=lambda e: page.go(HOME))
    return [ft.Row([logoutbtn, homebtn]), ft.Row([
        ft.Card(
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.ListTile(
                            leading=ft.Icon(ft.icons.MANAGE_ACCOUNTS),
                            title=ft.Text("Users"),
                            subtitle=ft.Text(
                                "Do smth with users"
                            ),
                        ),
                        ft.Row(
                            [ft.TextButton(
                                "Go", on_click=lambda e: page.go(ADMIN_USERS))],
                            alignment=ft.MainAxisAlignment.END,
                        ),
                    ]
                ),
                width=400,
                padding=10,
            )
        ),
        ft.Card(
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.ListTile(
                            leading=ft.Icon(ft.icons.LIST),
                            title=ft.Text("Statuses"),
                            subtitle=ft.Text(
                                "Do smth with statuses"
                            ),
                        ),
                        ft.Row(
                            [ft.TextButton(
                                "Go", on_click=lambda e: page.go(ADMIN_STATUS))],
                            alignment=ft.MainAxisAlignment.END,
                        ),
                    ]
                ),
                width=400,
                padding=10,
            )
        ),
        ft.Card(
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.ListTile(
                            leading=ft.Icon(ft.icons.SUPERVISOR_ACCOUNT),
                            title=ft.Text("Client Types"),
                            subtitle=ft.Text(
                                "Do smth with types of clients"
                            ),
                        ),
                        ft.Row(
                            [ft.TextButton(
                                "Go", on_click=lambda e: page.go(ADMIN_CLIENTTYPE))],
                            alignment=ft.MainAxisAlignment.END,
                        ),
                    ]
                ),
                width=400,
                padding=10,
            )
        )
    ])]
