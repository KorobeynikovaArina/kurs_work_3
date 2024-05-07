import flet as ft
from view.ROUTES import ADMIN, ADMIN_STATUS, ADMIN_STATUS_CREATE, HOME, LOGIN
from services.StatusService import StatusService


def admin_status_create(page: ft.Page):
    statusService = StatusService()
    troute = ft.TemplateRoute(page.route)
    is_update = False
    default_values = {"id": "", "title": ""}
    if troute.match(ADMIN_STATUS_CREATE+"/:id"):
        is_update = True
        id = troute.id
        status = statusService.get_by_id(id)
        default_values['id'] = status.id
        default_values['title'] = status.title

    def create_status(e):
        if status.value == '':
            return

        statusService.create(status.value)
        page.go(ADMIN_STATUS)

    def update_status(e):
        statusService.update(default_values['id'], title=status.value)
        page.go(ADMIN_STATUS)

    def logout(e):
        page.client_storage.remove('token')
        page.go(LOGIN)

    status = ft.TextField(hint_text='Title',
                          autofocus=True, value=default_values['title'])
    create_btn = ft.TextButton(
        text='Create', on_click=create_status, visible=not is_update)
    update_btn = ft.TextButton(
        text='Update', on_click=update_status, visible=is_update)

    logoutbtn = ft.TextButton(text='Logout', on_click=logout)
    homebtn = ft.TextButton(
        text="Home", on_click=lambda e: page.go(HOME))
    adminbtn = ft.TextButton(
        text="Admin panel", on_click=lambda e: page.go(ADMIN))

    return [ft.Row([logoutbtn, homebtn, adminbtn]),
            status,
            create_btn,
            update_btn]
