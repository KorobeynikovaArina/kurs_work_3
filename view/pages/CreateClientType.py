import flet as ft
from view.ROUTES import ADMIN, ADMIN_CLIENTTYPE, ADMIN_CLIENTTYPE_CREATE, HOME, LOGIN
from services.ClientTypeService import ClientTypeService


def admin_clienttype_create(page: ft.Page):
    clienttypeService = ClientTypeService()
    troute = ft.TemplateRoute(page.route)
    is_update = False
    default_values = {"id": "", "title": ""}

    if troute.match(ADMIN_CLIENTTYPE_CREATE+"/:id"):
        is_update = True
        id = troute.id
        client_type = clienttypeService.get_by_id(id)
        default_values["id"] = client_type.id
        default_values["title"] = client_type.title

    def create_clienttype(e):
        if client_type.value == "":
            return
        clienttypeService.create(client_type.value)
        page.go(ADMIN_CLIENTTYPE)

    def update_clienttype(e):
        clienttypeService.update(default_values["id"], title=client_type.value)
        page.go(ADMIN_CLIENTTYPE)

    def logout(e):
        page.client_storage.remove("token")
        page.go(LOGIN)

    def on_submit(e):
        if is_update:
            return update_clienttype(e)
        return create_clienttype(e)

    client_type = ft.TextField(hint_text="Title",
                               autofocus=True, on_submit=on_submit, value=default_values["title"])
    create_btn = ft.TextButton(
        text="Create", on_click=create_clienttype, visible=not is_update)
    update_btn = ft.TextButton(
        text="Update", on_click=update_clienttype, visible=is_update)

    logoutbtn = ft.TextButton(text="Logout", on_click=logout)
    homebtn = ft.TextButton(
        text="Home", on_click=lambda e: page.go(HOME))
    adminbtn = ft.TextButton(
        text="Admin panel", on_click=lambda e: page.go(ADMIN))
    clienttypesbtn = ft.TextButton(
        text="Client Types", on_click=lambda e: page.go(ADMIN_CLIENTTYPE))
    navbar = ft.Row([logoutbtn, homebtn, adminbtn, clienttypesbtn])
    return [navbar, client_type, create_btn, update_btn]
