from peewee import *
from dotenv import dotenv_values

c = dotenv_values()

db = SqliteDatabase(c['DB_NAME'])  # type: ignore


class BaseModel(Model):

    class Meta:
        database = db
