# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/maxk/Projects/OpenSource/arango-python/arango/__init__.py
# Compiled at: 2013-11-10 14:30:06
from arango.core import Connection

def create(**kwargs):
    """Connection factory"""
    conn = Connection(**kwargs)
    return conn.collection


c = Connection()
collection = c.collection