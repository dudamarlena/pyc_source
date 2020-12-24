# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: E:\Project\webapp\test\models.py
# Compiled at: 2017-08-31 11:09:07
import time
from mwebapp.orm import Model, IntegerField, StringField, FloatField

class User(Model):
    id = IntegerField(primary_key=True, updatable=False)
    name = StringField()
    email = StringField(updatable=False)
    passwd = StringField(default=lambda : '******')
    last_modified = FloatField()

    def pre_insert(self):
        self.last_modified = time.time()