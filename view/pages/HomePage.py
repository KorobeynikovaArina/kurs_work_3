import flet as ft

from services.OrderService import OrderService
from services.UserService import UserService
from view.ROUTES import ADMIN, LOGIN, ORDERS, ORDERS_CREATE


def home_page(page: ft.Page):
    page.title = "Издательство"
    troute = ft.TemplateRoute(page.route)

    userService = UserService()
    orderService = OrderService()

    token = page.client_storage.get("token")
    state = {
        'orders': [],
        'search_value': "",
        "search_by": ""
    }
    if troute.match(ORDERS+":by/:value"):
        by = troute.by
        value = troute.value
        state["orders"] = orderService.searchBy(value=value, by=by)
        state['search_value'] = value
        state['search_by'] = by
    else:
        state["orders"] = orderService.get_all()
    fields = {
        "id": "ID",
        "client": "client",
        "client_type": "client_type",
        "contact": "contact",
        "product_type": "product_type",
        "user": "user",
        "status": "status",
        "Update": "Update",
        "Delete": "Delete",
    }

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

    def search_order(e):
        by = search_by.value
        value = search_field.value
        if by and value:
            page.go(ORDERS+by+"/"+value)

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
            ft.DataColumn(ft.Text(fields[key])) for key in fields
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
                data=order.id,
            ) for order in state['orders']
        ],
    )
    search_field = ft.CupertinoTextField(
        placeholder_text="Search order",
        on_submit=search_order,
        value=state['search_value']
    )
    search_by_default = next(
        iter(fields)) if not state['search_by'] else state['search_by']
    search_by = ft.Dropdown(
        value=search_by_default,
        options=[ft.dropdown.Option(key=key, text=fields[key])
                 for key in fields],
        height=35,
        content_padding=10
    )
    search = ft.Row([
        search_field,
        search_by,
        ft.IconButton(ft.icons.SEARCH, on_click=search_order),
        ft.IconButton(ft.icons.RESTART_ALT, on_click=lambda e: page.go(ORDERS))
    ])
    navbar = ft.Row([logoutbtn, admin_panel, create_btn, search])
    return [navbar, tokentxt, rule, table]
