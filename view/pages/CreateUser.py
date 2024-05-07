import flet as ft
import jwt

from services.UserService import UserService
from view.ROUTES import ADMIN, ADMIN_USERS, ADMIN_USERS_CREATE, HOME, LOGIN


def admin_createuser_page(page: ft.Page):
    userService = UserService()
    troute = ft.TemplateRoute(page.route)
    is_update = False
    default_values = {
        "id": "",
        "username": "",
        "name": "",
        "password": "",
        "rule": False,
    }
    if troute.match(ADMIN_USERS_CREATE+"/:id"):
        is_update = True
        id = troute.id[1:]
        user = userService.get_by_id(id)
        default_values['id'] = user.id
        default_values["username"] = user.username
        default_values["name"] = user.name
        default_values["rule"] = bool(user.rule)

    def create_user(e):
        if username.value == '' or password.value == '' or name.value == '':
            return

        userService.create(username.value, password.value,
                           name.value, rule.value)
        page.go(ADMIN)

    def update_user(e):
        decoded_token = jwt.decode(
            page.client_storage.get('token'), key=None, options={"verify_signature": False})

        if decoded_token['username'] == default_values['username']:
            logout(e)
        userService.update(default_values['id'], username=username.value,
                           password=password.value,
                           name=name.value,
                           rule=rule.value)
        if not decoded_token['username'] == default_values['username']:
            page.go(ADMIN)

    def logout(e):
        token = page.client_storage.get('token')
        userService.logout(token)
        page.client_storage.remove('token')

        page.go(LOGIN)

    username = ft.TextField(hint_text='Username',
                            autofocus=True, value=default_values['username'])
    name = ft.TextField(hint_text='Name',
                        autofocus=True, value=default_values['name'])
    password = ft.TextField(hint_text='Password' if not is_update else "New password",
                            password=True, value=default_values['password'])
    rule = ft.Checkbox(label="Admin", value=default_values['rule'])
    create_btn = ft.TextButton(
        text='Create', on_click=create_user, visible=not is_update)
    update_btn = ft.TextButton(
        text='Update', on_click=update_user, visible=is_update)

    logoutbtn = ft.TextButton(text='Logout', on_click=logout)
    homebtn = ft.TextButton(
        text="Home", on_click=lambda e: page.go(HOME))
    adminbtn = ft.TextButton(
        text="Admin panel", on_click=lambda e: page.go(ADMIN))

    usersbtn = ft.TextButton(
        text="Users", on_click=lambda e: page.go(ADMIN_USERS))
    return [ft.Row([logoutbtn, homebtn, adminbtn, usersbtn]),
            username,
            name,
            password,
            rule,
            create_btn,
            update_btn]
