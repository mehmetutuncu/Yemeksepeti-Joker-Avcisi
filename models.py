from peewee import *

db = SqliteDatabase('yemeksepeti.db')


class User(Model):
    id = AutoField(primary_key=True)
    first_name = CharField(max_length=120)
    last_name = CharField(max_length=120)
    email = CharField(max_length=250)
    password = TextField()

    class Meta:
        database = db


class Region(Model):
    id = AutoField(primary_key=True)
    region_name = CharField(max_length=250)
    region_url = CharField(max_length=500)

    class Meta:
        database = db
