import flet as ft
from utils.RegexDict import RegexDict
from view.ROUTES import *
from view.pages.LoginPage import login_page
from view.pages.HomePage import home_page


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
    return d
