# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/maxk/Projects/OpenSource/arango-python/arango/__init__.py
# Compiled at: 2013-11-10 14:30:06
# Size of source mod 2**32: 193 bytes
from arango.core import Connection

def create(**kwargs):
    """Connection factory"""
    conn = Connection(**kwargs)
    return conn.collection


c = Connection()
collection = c.collection