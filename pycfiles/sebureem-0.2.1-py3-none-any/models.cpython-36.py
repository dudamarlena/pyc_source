# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/erwhann/Sources/Projets/sebureem/sebureem/models.py
# Compiled at: 2017-06-16 12:14:31
# Size of source mod 2**32: 626 bytes
"""Models
"""
from datetime import datetime
from peewee import Model
from peewee import CharField, TextField, BooleanField
from peewee import DateTimeField, ForeignKeyField
from sebureem import db
__all__ = [
 'Sebuks', 'Sebura']

class BaseModel(Model):

    class Meta:
        database = db


class Sebusik(BaseModel):
    pass


class Sebuks(BaseModel):
    name = CharField()
    locked = BooleanField(default=False)


class Sebura(BaseModel):
    text = TextField()
    date = DateTimeField(default=(datetime.now()))
    topic = ForeignKeyField(Sebuks, related_name='comments')
    published = BooleanField(default=False)