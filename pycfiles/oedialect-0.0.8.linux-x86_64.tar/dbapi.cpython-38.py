# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.8/site-packages/oedialect/dbapi.py
# Compiled at: 2018-09-20 08:32:21
# Size of source mod 2**32: 234 bytes
from psycopg2._psycopg import Error
from sqlalchemy.engine import Connection
from oedialect.engine import OEConnection

def connect(dsn=None, connection_factory=None, cursor_factory=None, **kwargs):
    return OEConnection(**kwargs)