from peewee import *
from models.BaseModel import BaseModel


class ClientType(BaseModel):
    title = CharField()
