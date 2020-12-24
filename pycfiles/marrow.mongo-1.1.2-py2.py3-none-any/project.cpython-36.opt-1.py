# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /marrow/mongo/param/project.py
# Compiled at: 2017-05-17 14:49:33
# Size of source mod 2**32: 928 bytes
"""Parameterized support akin to Django's ORM or MongoEngine."""
from __future__ import unicode_literals
from ...package.loader import traverse
from ...schema.compat import unicode

def P(Document, *fields, **kw):
    """Generate a MongoDB projection dictionary using the Django ORM style."""
    __always__ = kw.pop('__always__', set())
    projected = set()
    omitted = set()
    for field in fields:
        if field[0] in ('-', '!'):
            omitted.add(field[1:])
        else:
            if field[0] == '+':
                projected.add(field[1:])
            else:
                projected.add(field)

    if not projected:
        names = set(getattr(Document, '__projection__', Document.__fields__) or Document.__fields__)
        projected = {name for name in names - omitted}
    projected |= __always__
    if not projected:
        projected = {
         '_id'}
    return {unicode(traverse(Document, name, name)):True for name in projected}