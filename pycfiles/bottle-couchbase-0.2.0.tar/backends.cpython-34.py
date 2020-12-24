# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/fede/newhome/projects/bottle-cork/tests/cork/backends.py
# Compiled at: 2015-04-26 05:39:16
# Size of source mod 2**32: 458 bytes
__doc__ = '\n.. module:: backends\n   :synopsis: Backends API - used to make backends available for importing\n'
from .json_backend import JsonBackend
from .mongodb_backend import MongoDBBackend
from .sqlalchemy_backend import SqlAlchemyBackend
from .sqlite_backend import SQLiteBackend