import jwt
from models.User import User
from dotenv import dotenv_values

c = dotenv_values()
SECRET = c['SECRET']


class UserAllreadyExist(Exception):
    def __init__(self):
        self.message = 'User allready exist'


class UserService():
    def __init__(self) -> None:
        self.UserModel = User

    def create(self, username, password, name, rule):
        hash_password = self._get_hashed_password(password)
        eu = self.UserModel.get_or_none(self.UserModel.username == username)
        if eu:
            raise UserAllreadyExist()
        return self.UserModel.create(username=username, name=name, rule=rule, password=hash_password)

    def create_if_not_exist(self, username, password, name, rule):
        try:
            return self.create(username, password, name, rule)
        except Exception as e:
            return

    def update(self, id: int, *args, **kwargs):
        """
        accept username, password, name, rule in kwargs
        e.g. update(username="nnnn"....)
        """
        username = kwargs.get('username', None)
        password = kwargs.get('password', None)
        name = kwargs.get('name', None)
        rule = kwargs.get('rule', None)

        user = {}

        if username:
            # check if username allready exist
            user[self.UserModel.username] = username
        if password:
            hash_password = self._get_hashed_password(password)
            user[self.UserModel.password] = hash_password
        if name:
            user[self.UserModel.name] = name
        if rule is not None:
            user[self.UserModel.rule] = rule

        self.UserModel.update(user).where(self.UserModel.id == id).execute()

    def delete(self, id: int):
        user = self.UserModel.get_by_id(id)
        user.delete_instance(recursive=True)

    def login(self, username, password):
        try:
            user: User = self.UserModel.get(username=username)
        except:
            return False
        if self._get_hashed_password(password) == user.password:
            token = jwt.encode(
                {"username": user.username, "rule": user.rule}, SECRET, algorithm="HS256")
            user.token = token
            user.save()
            return token

    def logout(self, token):
        decode_token = jwt.decode(token, SECRET, algorithms=["HS256"])
        user: User = self.UserModel.get_or_none(
            username=decode_token['username'])
        if not user:
            return
        user.token = ''
        user.save()

    def is_admin(self, token):
        if not token:
            return False
        decode_token = jwt.decode(token, SECRET, algorithms=["HS256"])
        user: User = self.UserModel.get(username=decode_token['username'])
        if not token == user.token:
            return False
        if decode_token['rule']:
            return True
        return False

    def get_all(self):
        return [user for user in self.UserModel.select()]

    def get_by_id(self, id: int):
        return self.UserModel.get_by_id(id)

    def get_user_by_token(self, token):
        if not token:
            return False
        decode_token = jwt.decode(token, SECRET, algorithms=["HS256"])
        user: User = self.UserModel.get(username=decode_token['username'])
        return user

    def _get_hashed_password(self, password: str):
        return password
