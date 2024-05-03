import flet as ft

from view.ROUTES import HOME, LOGIN
from view.views import views_handler


def base_page(page: ft.Page):
    page.title = "Apps"

    def route_change(route):
        print("Page:", page.route)
        page.views.clear()
        page.views.append(
            views_handler(page)[page.route]
        )
        page.update()

    page.on_route_change = route_change
    token = page.client_storage.get('token')
    if not token:
        page.go(LOGIN)
    else:
        page.go(HOME)
