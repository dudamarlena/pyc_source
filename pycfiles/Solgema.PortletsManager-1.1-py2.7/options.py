# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/Solgema/PortletsManager/options.py
# Compiled at: 2011-09-02 07:59:09
"""
$Id: options.py 1516 2008-05-03 12:57:53Z cwithers $
"""
try:
    from zope.annotation import IAnnotations
except ImportError:
    from zope.app.annotation import IAnnotations

from persistent.dict import PersistentDict
from persistent import Persistent
from zope import schema
from zope.interface import classImplements, implements
import interfaces
_marker = object()

class PersistentOptions(object):
    implements(interfaces.IPersistentOptions)
    _storage = None

    def __init__(self, context):
        self.context = context

    def storage(self, name=None):
        """ name if given is the key of a persistent dictionary off of
        the annotation.
        """
        if self._storage is None:
            annotations = IAnnotations(self)
            self._storage = annotations.get(self.annotation_key, None)
            if self._storage is None:
                annotations[self.annotation_key] = self._storage = PersistentDict()
        if name is None:
            return self._storage
        else:
            if name in self._storage:
                return self._storage[name]
            self._storage[name] = PersistentDict()
            return self._storage[name]

    def getProperty(self, property_name):
        return self.storage().get(property_name)

    def getFieldProperty(self, field):
        value = self.storage().get(field.__name__, _marker)
        if value is _marker:
            return field.default
        return value

    def setProperty(self, property_name, property_value):
        self.storage()[property_name] = property_value

    def nullProperty(self, *args):
        return

    def wire(cls, name, key, *interfaces, **options):
        fields = {}
        bases = (
         cls,) + options.get('bases', ())
        for iface in interfaces:
            for field in schema.getFields(iface).values():
                fields[field.__name__] = property(lambda self, field=field: self.getFieldProperty(field), lambda self, value, field_name=field.__name__: self.setProperty(field_name, value))

        new_class = type(name, bases, fields)
        cls.annotation_key = key
        classImplements(new_class, interfaces)
        return new_class

    wire = classmethod(wire)