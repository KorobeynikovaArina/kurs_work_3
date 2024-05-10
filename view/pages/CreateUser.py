import flet as ft
import jwt

from services.UserService import UserAllreadyExist, UserService
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
        "is_username_changed": False
    }
    text_status = ft.Text(value="", color="red")

    if troute.match(ADMIN_USERS_CREATE+"/:id"):
        is_update = True
        id = troute.id[1:]
        user = userService.get_by_id(id)
        default_values["id"] = user.id
        default_values["username"] = user.username
        default_values["name"] = user.name
        default_values["rule"] = bool(user.rule)

    def create_user(e):
        if username.value == "" or password.value == "" or name.value == "":
            return
        try:
            userService.create(username.value, password.value,
                               name.value, rule.value)
        except UserAllreadyExist as e:
            text_status.value = "UserAllreadiExist"
            page.update()
            return

        page.go(ADMIN)

    def update_user(e):
        decoded_token = jwt.decode(
            page.client_storage.get("token"), key=None, options={"verify_signature": False})

        if decoded_token["username"] == default_values["username"]:
            logout(e)

        try:
            userService.update(default_values["id"],
                               username=username.value if default_values["is_username_changed"] else None,
                               password=password.value,
                               name=name.value,
                               rule=rule.value)
        except UserAllreadyExist as e:
            text_status.value = "UserAlreadyExist"
            page.update()
            return
        if not decoded_token["username"] == default_values["username"]:
            page.go(ADMIN_USERS)

    def logout(e):
        token = page.client_storage.get("token")
        userService.logout(token)
        page.client_storage.remove("token")

        page.go(LOGIN)

    def on_username_changed(e):
        default_values["is_username_changed"] = True

    username = ft.TextField(hint_text="Username",
                            autofocus=True, value=default_values["username"],
                            on_change=on_username_changed, on_submit=update_user if is_update else create_user)
    name = ft.TextField(hint_text="Name",
                        autofocus=True, value=default_values["name"], on_submit=update_user if is_update else create_user)
    password = ft.TextField(hint_text="Password" if not is_update else "New password",
                            password=True, value=default_values["password"], on_submit=update_user if is_update else create_user)
    rule = ft.Checkbox(label="Admin", value=default_values["rule"])

    create_btn = ft.TextButton(
        text="Create", on_click=create_user, visible=not is_update)
    update_btn = ft.TextButton(
        text="Update", on_click=update_user, visible=is_update)

    logoutbtn = ft.TextButton(text="Logout", on_click=logout)
    homebtn = ft.TextButton(
        text="Home", on_click=lambda e: page.go(HOME))
    adminbtn = ft.TextButton(
        text="Admin panel", on_click=lambda e: page.go(ADMIN))

    usersbtn = ft.TextButton(
        text="Users", on_click=lambda e: page.go(ADMIN_USERS))
    navbar = ft.Row([logoutbtn, homebtn, adminbtn, usersbtn])
    return [navbar,
            username,
            name,
            password,
            rule,
            create_btn,
            update_btn,
            text_status]
