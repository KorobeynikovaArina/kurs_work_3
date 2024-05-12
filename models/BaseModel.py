from os import path
from peewee import *
from dotenv import dotenv_values
from appdirs import *
from playhouse.signals import Model
c = dotenv_values()

db_path = path.join(user_data_dir(
    c["APP_NAME"], c["APP_AUTHOR"]), c['DB_NAME'])

# db = SqliteDatabase(db_path)
db = SqliteDatabase(c['DB_NAME'])


class BaseModel(Model):

    class Meta:
        database = db
