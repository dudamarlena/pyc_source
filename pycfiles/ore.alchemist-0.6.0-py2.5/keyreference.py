# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/ore/alchemist/keyreference.py
# Compiled at: 2008-09-11 20:29:53
"""
Author: Kapil Thangavelu <kapil.foss@gmail.com>

$Id: keyreference.py 299 2008-05-23 20:31:48Z kapilt $
"""
import zope.interface
from zope.app.keyreference.interfaces import IKeyReference
from zope.dottedname.resolve import resolve
from ore.alchemist import Session, named

def getPrimaryKey(object):
    values = []
    marker = object()
    for column in object.c:
        if column.primary_key:
            value = getattr(object, column.name, marker)
            if value is marker or value is None:
                raise zope.app.keyreference.interfaces.NotYet(object)
            values.append(value)

    return tuple(values)


class AlchemistKeyReference(object):
    zope.interface.implements(IKeyReference)
    key_type_id = 'ore.alchemist.keyreference'

    def __init__(self, object):
        self.klass = named(object.__class__)
        primary_key = getPrimaryKey(object)
        if len(primary_key) == 1:
            self.primary_key = primary_key[0]
        else:
            self.primary_key = primary_key

    def __call__(self):
        klass = resolve(self.klass)
        session = Session()
        query = session.query(klass)
        return query.get(self.primary_key)

    def __hash__(self):
        return hash((self.klass, self.primary_key))

    def __cmp__(self, other):
        if self.key_type_id == other.key:
            return cmp((self.klass, self.primary_key), (
             other.klass, other.primary_key))
        return cmp(self.key_type_id, other.key_type_id)