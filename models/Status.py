from peewee import *
from models.BaseModel import BaseModel


class Status(BaseModel):
    title = CharField(max_length=50)
