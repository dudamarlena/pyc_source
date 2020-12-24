# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/charles/code/flask-peewee/example/config.py
# Compiled at: 2018-01-17 11:50:43


class Configuration(object):
    DATABASE = {'name': 'example.db', 
       'engine': 'peewee.SqliteDatabase', 
       'check_same_thread': False}
    DEBUG = True
    SECRET_KEY = 'shhhh'