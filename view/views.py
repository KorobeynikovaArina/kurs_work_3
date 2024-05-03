import flet as ft
from utils.RegexDict import RegexDict
from view.ROUTES import *
from view.pages.LoginPage import login_page
from view.pages.HomePage import home_page
from view.pages.AdminPage import admin_page


def views_handler(page: ft.Page):
    d = RegexDict()

    d[LOGIN] = ft.View(
        route=LOGIN,
        controls=login_page(page)
    )
    d[HOME] = ft.View(
        route=HOME,
        controls=home_page(page),
    )
    d[ADMIN] = ft.View(
        route=ADMIN,
        controls=admin_page(page),
    )
    return d
