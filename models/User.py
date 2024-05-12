from os import makedirs, path
from peewee import *
from models.BaseModel import BaseModel
from playhouse.signals import *
from appdirs import *
from dotenv import dotenv_values

c = dotenv_values()


class User(BaseModel):
    username = CharField()
    password = CharField()
    name = CharField()
    token = CharField(default="")
    rule = IntegerField()  # 0 - meneger, 1 - admin
    upload_dir = TextField(default="")


@post_save(sender=User)
def post_user_save(sender, instance, created):
    if instance.upload_dir != "":
        return
    user_dir = user_data_dir(c["APP_NAME"], c["APP_AUTHOR"])
    upload_dir = path.join(user_dir, str(instance.id))
    if not path.exists(upload_dir):
        makedirs(upload_dir)
    instance.upload_dir = upload_dir
    instance.save()
