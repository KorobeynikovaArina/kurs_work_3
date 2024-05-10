import flet as ft
import jwt

from services.OrderService import OrderService
from services.UserService import UserService
from view.ROUTES import ADMIN, LOGIN


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

    orders = orderService.get_all()

    tokentxt = ft.Text(token)
    try:
        is_admin = userService.is_admin(token)
    except userService.UserModel.DoesNotExist as e:
        return logout("")

    rule = ft.Text(("meneger", "admin")[is_admin])
    logoutbtn = ft.TextButton(text="Logout", on_click=logout)
    admin_panel = ft.TextButton(
        text="Admin panel", on_click=lambda e: page.go(ADMIN), visible=is_admin)

    table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("client")),
            ft.DataColumn(ft.Text("client_type")),
            ft.DataColumn(ft.Text("contact")),
            ft.DataColumn(ft.Text("product_type")),
            ft.DataColumn(ft.Text("material_filepath")),
            ft.DataColumn(ft.Text("user")),
            ft.DataColumn(ft.Text("status")),
        ],
        rows=[
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(order.client)),
                    ft.DataCell(ft.Text(order.client_type)),
                    ft.DataCell(ft.Text(order.contact)),
                    ft.DataCell(ft.Text(order.product_type)),
                    ft.DataCell(ft.Text(order.material_filepath)),
                    ft.DataCell(ft.Text(order.user)),
                    ft.DataCell(ft.Text(order.status)),
                ],
            ) for order in orders
        ],
    )
    navbar = ft.Row([logoutbtn, admin_panel])
    return [navbar, tokentxt, rule, table]
