# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/Products/UpfrontContacts/schemapatch.py
# Compiled at: 2010-03-10 13:47:45
__doc__ = ' This module monkey patches AT schemas to generate events when fields\n    are added or removed from a schema.\n    \n    This is necessary to invalidate schema caches.\n'
from zope import event
from zope.app.event import objectevent
from Products.Archetypes.Schema import Schema, ManagedSchema
from Products.Archetypes.interfaces import IManagedSchema
from Products.Archetypes.VariableSchemaSupport import VariableSchemaSupport
from Products.Archetypes.VariableSchemaSupport import VarClassGen
from Products.Archetypes.VariableSchemaSupport import schemadict

def addField(self, field):
    Schema.addField(self, field)
    event.notify(objectevent.ObjectModifiedEvent(self))


ManagedSchema.addField = addField

def delField(self, name):
    Schema.delField(self, name)
    event.notify(objectevent.ObjectModifiedEvent(self))


ManagedSchema.delField = delField

def getAndPrepareSchema(self):
    """ Use the builtin 'id' to generate a key for a schema
    """
    s = self.getSchema()
    key = id(s)
    if schemadict.has_key(key):
        schema = schemadict[key]
    else:
        schemadict[key] = s
        schema = schemadict[key]
        g = VarClassGen(schema)
        g.generateClass(self.__class__)
    return schema


VariableSchemaSupport.getAndPrepareSchema = getAndPrepareSchema

def invalidateSchema(event):
    if IManagedSchema.providedBy(event.object):
        key = id(event.object)
        if schemadict.has_key(key):
            del schemadict[key]