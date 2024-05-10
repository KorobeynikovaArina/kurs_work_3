from peewee import *
from models.BaseModel import BaseModel


class User(BaseModel):
    username = CharField()
    password = CharField()
    name = CharField()
    token = CharField(default="")
    rule = IntegerField()  # 0 - meneger, 1 - admin
