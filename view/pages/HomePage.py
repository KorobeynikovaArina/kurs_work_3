import flet as ft

from services.OrderService import OrderService
from services.UserService import UserService
from view.ROUTES import ADMIN, LOGIN, ORDERS_CREATE


def home_page(page: ft.Page):
    page.title = "Издательство"
    userService = UserService()
    orderService = OrderService()

    token = page.client_storage.get("token")

    def logout(e):
        token = page.client_storage.get("token")
        userService.logout(token)
        page.client_storage.remove("token")

        page.go(LOGIN)

    def go_edit(e):
        page.go(ORDERS_CREATE+f"/:{e.control.data}")

    def on_delete(e):
        orderService.delete(e.control.data)
        for row in table.rows:
            if row.data == e.control.data:
                table.rows.remove(row)
                page.update()
                break

    orders = orderService.get_all()

    current_user = userService.get_user_by_token(
        page.client_storage.get("token"))
    if not current_user:
        return

    tokentxt = ft.Text(token)
    try:
        is_admin = userService.is_admin(token)
    except userService.UserModel.DoesNotExist as e:
        return logout("")

    rule = ft.Text(("meneger", "admin")[is_admin])
    logoutbtn = ft.TextButton(text="Logout", on_click=logout)
    admin_panel = ft.TextButton(
        text="Admin panel", on_click=lambda e: page.go(ADMIN), visible=is_admin)
    create_btn = ft.OutlinedButton(
        text="Create order", on_click=lambda e: page.go(ORDERS_CREATE), icon=ft.icons.ADD, icon_color=ft.colors.GREEN_400)
    table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("id")),
            ft.DataColumn(ft.Text("client")),
            ft.DataColumn(ft.Text("client_type")),
            ft.DataColumn(ft.Text("contact")),
            ft.DataColumn(ft.Text("product_type")),
            ft.DataColumn(ft.Text("user")),
            ft.DataColumn(ft.Text("status")),
            ft.DataColumn(ft.Text("Update")),
            ft.DataColumn(ft.Text("Delete"))
        ],
        rows=[
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(order.id)),
                    ft.DataCell(ft.Text(order.client)),
                    ft.DataCell(ft.Text(order.client_type.title)),
                    ft.DataCell(ft.Text(order.contact)),
                    ft.DataCell(ft.Text(order.product_type)),
                    ft.DataCell(ft.Text(order.user.name)),
                    ft.DataCell(ft.Text(order.status.title)),
                    ft.DataCell(ft.IconButton(
                        ft.icons.EDIT, ft.colors.GREEN, on_click=go_edit, data=order.id)),
                    ft.DataCell(ft.IconButton(
                        ft.icons.DELETE, ft.colors.GREY if order.user.id != current_user.id and not is_admin else ft.colors.RED, on_click=on_delete, data=order.id, disabled=order.user.id != current_user.id or not is_admin))
                ],
                data=order.id
            ) for order in orders
        ],
    )
    navbar = ft.Row([logoutbtn, admin_panel, create_btn])
    return [navbar, tokentxt, rule, table]
