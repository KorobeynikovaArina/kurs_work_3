import flet as ft
from utils.RegexDict import RegexDict
from view.ROUTES import *
from view.pages.AdminStatusPage import admin_status_page
from view.pages.CreateStatus import admin_status_create
from view.pages.LoginPage import login_page
from view.pages.HomePage import home_page
from view.pages.AdminPage import admin_page
from view.pages.AdminUsersPage import admin_users_page
from view.pages.CreateUser import admin_createuser_page


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
    d[ADMIN_USERS] = ft.View(
        route=ADMIN_USERS,
        controls=admin_users_page(page),
    )
    d[ADMIN_USERS_CREATE] = ft.View(
        route=ADMIN_USERS_CREATE,
        controls=admin_createuser_page(page)
    )
    d[ADMIN_USERS_CREATE + "/.*"] = ft.View(
        route=ADMIN_USERS_CREATE,
        controls=admin_createuser_page(page)
    )
    d[ADMIN_STATUS] = ft.View(
        route=ADMIN_STATUS,
        controls=admin_status_page(page)
    )
    d[ADMIN_STATUS_CREATE] = ft.View(
        route=ADMIN_STATUS_CREATE,
        controls=admin_status_create(page)
    )
    d[ADMIN_STATUS] = ft.View(
        route=ADMIN_STATUS,
        controls=admin_status_page(page)
    )
    d[ADMIN_STATUS_CREATE+"/.*"] = ft.View(
        route=ADMIN_STATUS_CREATE,
        controls=admin_status_create(page)
    )
    return d
