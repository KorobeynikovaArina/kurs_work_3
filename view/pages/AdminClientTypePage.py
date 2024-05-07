from view.ROUTES import ADMIN, ADMIN_CLIENTTYPE_CREATE, HOME, LOGIN
from services.ClientTypeService import ClientTypeService
import flet as ft


def admin_clienttype_page(page: ft.Page):
    clienttypeService = ClientTypeService()

    def logout(e):
        page.client_storage.remove('token')
        page.go(LOGIN)

    def go_edit(e):
        page.go(ADMIN_CLIENTTYPE_CREATE+f"/{e.control.data}")

    def on_delete(e):
        clienttypeService.delete(e.control.data)
        for row in table.rows:
            if row.data == e.control.data:
                table.rows.remove(row)
                page.update()
                break
    client_types = clienttypeService.get_all()

    logoutbtn = ft.TextButton(text='Logout', on_click=logout)
    homebtn = ft.TextButton(
        text="Home", on_click=lambda e: page.go(HOME))
    createbtn = ft.OutlinedButton(
        text="Create client type", on_click=lambda e: page.go(ADMIN_CLIENTTYPE_CREATE), icon=ft.icons.ADD, icon_color=ft.colors.GREEN_400)
    adminbtn = ft.TextButton(
        text="Admin panel", on_click=lambda e: page.go(ADMIN))

    table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Title")),
            ft.DataColumn(ft.Text("Do")),
        ],
        rows=[ft.DataRow(
            cells=[
                ft.DataCell(ft.Text(client_type.title)),
                ft.DataCell(ft.Row([ft.IconButton(ft.icons.EDIT,
                                                  ft.colors.GREEN, on_click=go_edit, data=client_type.id), ft.IconButton(ft.icons.DELETE,
                                                                                                                         ft.colors.RED, on_click=on_delete, data=client_type.id)])),

            ], data=client_type.id
        ) for client_type in client_types],
    )

    return [ft.Row([logoutbtn, homebtn, adminbtn, createbtn]), table]
