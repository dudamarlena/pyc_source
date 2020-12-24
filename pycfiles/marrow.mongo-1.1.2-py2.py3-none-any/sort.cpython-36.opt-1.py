# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /marrow/mongo/param/sort.py
# Compiled at: 2017-05-17 14:49:33
# Size of source mod 2**32: 817 bytes
"""Parameterized support akin to Django's ORM or MongoEngine."""
from __future__ import unicode_literals
from pymongo import ASCENDING, DESCENDING
from ...package.loader import traverse

def S(Document, *fields):
    """Generate a MongoDB sort order list using the Django ORM style."""
    result = []
    for field in fields:
        if isinstance(field, tuple):
            field, direction = field
            result.append((field, direction))
        else:
            direction = ASCENDING
            if not field.startswith('__'):
                field = field.replace('__', '.')
            if field[0] == '-':
                direction = DESCENDING
            if field[0] in ('+', '-'):
                field = field[1:]
            _field = traverse(Document, field, default=None)
            result.append((~_field if _field else field, direction))

    return result