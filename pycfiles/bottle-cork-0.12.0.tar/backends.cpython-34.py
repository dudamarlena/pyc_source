# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/fede/newhome/projects/bottle-cork/tests/cork/backends.py
# Compiled at: 2015-04-26 05:39:16
# Size of source mod 2**32: 458 bytes
"""
.. module:: backends
   :synopsis: Backends API - used to make backends available for importing
"""
from .json_backend import JsonBackend
from .mongodb_backend import MongoDBBackend
from .sqlalchemy_backend import SqlAlchemyBackend
from .sqlite_backend import SQLiteBackend