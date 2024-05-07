from view.ROUTES import ADMIN, ADMIN_STATUS_CREATE, HOME, LOGIN
from services.StatusService import StatusService
import flet as ft


def admin_status_page(page: ft.Page):
    statusService = StatusService()

    def logout(e):
        page.client_storage.remove('token')
        page.go(LOGIN)

    def go_edit(e):
        page.go(ADMIN_STATUS_CREATE+f"/{e.control.data}")

    def on_delete(e):
        statusService.delete(e.control.data)
        for row in table.rows:
            if row.data == e.control.data:
                table.rows.remove(row)
                page.update()
                break
    statuses = statusService.get_all()

    logoutbtn = ft.TextButton(text='Logout', on_click=logout)
    homebtn = ft.TextButton(
        text="Home", on_click=lambda e: page.go(HOME))
    createbtn = ft.TextButton(
        text="Create status", on_click=lambda e: page.go(ADMIN_STATUS_CREATE))
    adminbtn = ft.TextButton(
        text="Admin panel", on_click=lambda e: page.go(ADMIN))

    table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Title")),
            ft.DataColumn(ft.Text("Do")),
        ],
        rows=[ft.DataRow(
            cells=[
                ft.DataCell(ft.Text(status.title)),
                ft.DataCell(ft.Row([ft.IconButton(ft.icons.EDIT,
                                                  ft.colors.GREEN, on_click=go_edit, data=status.id), ft.IconButton(ft.icons.DELETE,
                                                                                                                    ft.colors.RED, on_click=on_delete, data=status.id)])),

            ], data=status.id
        ) for status in statuses],
    )

    return [ft.Row([logoutbtn, homebtn, adminbtn, createbtn]), table]
