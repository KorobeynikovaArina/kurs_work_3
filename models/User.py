from peewee import *
from models.BaseModel import BaseModel


class User(BaseModel):
    username = CharField()
    password = CharField()
    name = CharField()
    token = CharField(default="")
    # 0 - meneger, 1 - admin
    rule = IntegerField()
