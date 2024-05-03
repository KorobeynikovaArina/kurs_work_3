from peewee import *

from models.ClientType import ClientType
from models.User import User
from models.BaseModel import BaseModel
from models.Status import Status


class Order(BaseModel):
    client = CharField()
    client_type = ForeignKeyField(ClientType)
    contact = CharField()
    product_type = CharField()
    material_filepath = CharField()
    user = ForeignKeyField(User, backref='orders')
    status = ForeignKeyField(Status, backref='orders')
