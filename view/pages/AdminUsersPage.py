import flet as ft

from services.UserService import UserService
from view.ROUTES import ADMIN, ADMIN_USERS_CREATE, HOME, LOGIN


def admin_users_page(page: ft.Page):
    userService = UserService()

    def logout(e):
        page.client_storage.remove("token")
        page.go(LOGIN)

    def go_edit(e):
        page.go(ADMIN_USERS_CREATE+f"/:{e.control.data}")

    def on_delete(e):
        userService.delete(e.control.data)
        for row in table.rows:
            if row.data == e.control.data:
                table.rows.remove(row)
                page.update()
                return

    users = userService.get_all()

    current_user = userService.get_user_by_token(
        page.client_storage.get("token"))
    if not current_user:
        return

    logoutbtn = ft.TextButton(text="Logout", on_click=logout)
    homebtn = ft.TextButton(
        text="Home", on_click=lambda e: page.go(HOME))
    createbtn = ft.OutlinedButton(
        text="Create user", on_click=lambda e: page.go(ADMIN_USERS_CREATE), icon=ft.icons.ADD, icon_color=ft.colors.GREEN_400)
    adminbtn = ft.TextButton(
        text="Admin panel", on_click=lambda e: page.go(ADMIN))

    table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Username")),
            ft.DataColumn(ft.Text("Name")),
            ft.DataColumn(ft.Text("Rule"), numeric=True),
            ft.DataColumn(ft.Text("Update")),
            ft.DataColumn(ft.Text("Delete"))
        ],
        rows=[
            ft.DataRow(
                color=ft.colors.BLUE_100 if user.id == current_user.id else None,
                cells=[
                    ft.DataCell(ft.Text(user.username)),
                    ft.DataCell(ft.Text(user.name)),
                    ft.DataCell(ft.Text(user.rule)),
                    ft.DataCell(ft.IconButton(
                        ft.icons.EDIT, ft.colors.GREEN, on_click=go_edit, data=user.id)),
                    ft.DataCell(ft.IconButton(
                        ft.icons.DELETE, ft.colors.GREY if user.id == current_user.id else ft.colors.RED, on_click=on_delete, data=user.id, disabled=user.id == current_user.id)),
                ],
                data=user.id,
            ) for user in users
        ],

    )
    navbar = ft.Row([logoutbtn, homebtn, adminbtn, createbtn])
    return [navbar, table]
