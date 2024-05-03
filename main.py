import flet as ft
from models import BaseModel
from models.ClientType import ClientType
from models.Order import Order
from models.Status import Status
from models.User import User
from services.UserService import UserService
from view.app import base_page


def create_admin():
    u = UserService()
    u.create_if_not_exist("admin", "1234", "admin misha", 1)


def main():
    BaseModel.db.connect()
    BaseModel.db.create_tables([User, Order, Status, ClientType])

    create_admin()

    ft.app(target=base_page)


main()
