
from peewee import *

from models.ClientType import ClientType as ClientTypeOriginal
from models.Order import Order as OrderOriginal
from models.Status import Status as StatusOriginal
from models.User import User as UserOriginal
from services.ClientTypeService import ClientTypeService as ClientTypeServiceOriginal
from services.OrderService import OrderService as OrderServiceOriginal
from services.StatusService import StatusService as StatusServiceOriginal
from services.UserService import UserAllreadyExist, UserService as UserServiceOriginal


def test(name, fn):
    """
    утилита для запуска одного теста
    """
    db.connect()
    db.create_tables([User, Order, Status, ClientType])
    print("\033[92m✓\033[0m" if fn() else "\033[91m×\033[0m", "|", name)
    db.drop_tables([User, Order, Status, ClientType])
    db.close()


def run_tests(fns):
    """
    утилита для запуска тестов
    """
    for fn in fns:
        print(f"----{fn.__name__}----")
        fn()


# Создание моковых моделей и сервисов, чтобы они работали с другой БД
db = SqliteDatabase(":memory:")


class Order(OrderOriginal):
    class Meta:
        database = db


class OrderService(OrderServiceOriginal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.OrderModel = Order


class Status(StatusOriginal):
    class Meta:
        database = db


class StatusService(StatusServiceOriginal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.StatusModel = Status


class User(UserOriginal):
    class Meta:
        database = db


class UserService(UserServiceOriginal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.UserModel = User


class ClientType(ClientTypeOriginal):
    class Meta:
        database = db


class ClientTypeService(ClientTypeServiceOriginal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.ClientTypeModel = ClientType

# ================= Тестировние ==================


class TestUserService():
    def create_test(self):
        us = UserService()
        u = us.create("misha1425", "1234", "misha misha", 1)
        if u.username == "misha1425":
            return True

    def create_existing_user(self):
        us = UserService()
        us.create("misha1425", "1234", "misha misha", 1)
        try:
            us.create("misha1425", "1234", "misha misha", 1)
            return False
        except UserAllreadyExist as e:
            return True

    def test_create_if_not_exist(self):
        pass

    def test_update(self):
        pass

    def test_delete(self):
        pass

    def test_login(self):
        pass

    def test_is_admin(self):
        pass

    def test_get_all(self):
        pass

    def test_get_by_id(self):
        pass

    def test__get_hashed_password(self):
        pass


class TestStatusService():
    pass


class TestClietTypeService():
    pass


class TestOrderService():
    def test_create(self):
        pass

    def test_update(self):
        pass

    def test_delete(self):
        pass

    def test_get_all(self):
        pass


def test_userservice():
    """
    тестирование UserService
    """
    TUS = TestUserService()
    test("Создает пользователя", TUS.create_test)
    test("Не создает пользователя с одинаковым логином", TUS.create_existing_user)
    test("test_create_if_not_exist", TUS.test_create_if_not_exist)
    test("test_update", TUS.test_update)
    test("test_delete", TUS.test_delete)
    test("test_login", TUS.test_login)
    # test("logout", TUS.logout)
    test("test_is_admin", TUS.test_is_admin)
    test("test_get_all", TUS.test_get_all)
    test("test_get_by_id", TUS.test_get_by_id)
    test("test__get_hashed_password", TUS.test__get_hashed_password)


def test_statusservice():
    """
    тестирование StatusService
    """
    pass


# Запуск тестов
run_tests([
    test_userservice,
    test_statusservice,
])
