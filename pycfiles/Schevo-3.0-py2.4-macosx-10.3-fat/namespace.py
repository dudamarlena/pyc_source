# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/schevo/namespace.py
# Compiled at: 2007-03-21 14:34:41
"""Namespace extension classes.

For copyright, license, and warranty, see bottom of file.
"""
import sys
from schevo import base
from schevo.fieldspec import FieldDefinition
from schevo.label import label_from_name
from schevo.lib import optimize
EVOLVING = False
SCHEMADEF = None
SCHEMADB = None

class SchemaDefinition(object):
    """Keeps track of information about a schema during import."""
    __module__ = __name__

    def __init__(self):
        self.E = EntityClasses()
        self.F = FieldClasses()
        self.f = FieldConstructors()
        self.Q = QueryClasses()
        self.q = DatabaseQueries()
        self.T = TransactionClasses()
        self.t = DatabaseTransactions()
        self.V = ViewClasses()
        self.relationships = {}


class Fields(object):
    """A namespace that gives attribute access to an object's field
    instances."""
    __module__ = __name__

    def __init__(self, obj):
        self.__dict__['_obj'] = obj

    def __delattr__(self, name):
        f = self._obj._field_map
        if name not in f:
            raise AttributeError(name)
        del f[name]

    def __getattr__(self, name):
        return self._obj._field_map[name]

    def __getitem__(self, name):
        return self.__getattr__(name)

    def __iter__(self):
        return iter(self._obj._field_map)

    def __setattr__(self, name, value):
        field_map = self._obj._field_map
        if name in field_map:
            raise AttributeError('%r already exists.' % name)
        if isinstance(value, FieldDefinition):
            value = value.field(name=name, instance=self._obj)
        elif isinstance(value, base.Field):
            value._instance = self._obj
            if not value.label:
                value.label = label_from_name(name)
        else:
            msg = '%r is not a Field or FieldDefinition instance.' % value
            raise ValueError(msg)
        field_map[name] = value

    def _getAttributeNames(self):
        """Return list of hidden attributes to extend introspection."""
        return sorted(self._obj._field_map.keys())


class NamespaceExtension(object):
    """A namespace extension with index syntax support."""
    __module__ = __name__
    __slots__ = [
     '_d']
    _readonly = True

    def __init__(self):
        self._d = {}

    def __contains__(self, name):
        return name in self._d

    def __getattr__(self, name):
        try:
            return self._d[name]
        except KeyError:
            raise AttributeError(name)

    def __getitem__(self, name):
        return self._d[name]

    def __iter__(self):
        return iter(self._d)

    def __len__(self):
        return len(self._d)

    def __setattr__(self, name, value):
        if name in self.__slots__:
            object.__setattr__(self, name, value)
        elif self._readonly:
            msg = 'Readonly namespace, cannot set %r to %r.' % (name, value)
            raise AttributeError(msg)
        else:
            self._d[name] = value

    def _getAttributeNames(self):
        """Return list of hidden attributes to extend introspection."""
        return sorted(self._d.keys())

    def _set(self, name, value):
        """Backdoor method to set `name` to `value`."""
        self._d[name] = value


class DatabaseQueries(NamespaceExtension):
    """A namespace of database-level queries."""
    __module__ = __name__
    __slots__ = NamespaceExtension.__slots__


class DatabaseTransactions(NamespaceExtension):
    """A namespace of database-level transactions."""
    __module__ = __name__
    __slots__ = NamespaceExtension.__slots__


class EntityClasses(NamespaceExtension):
    """A namespace of Entity classes."""
    __module__ = __name__
    __slots__ = NamespaceExtension.__slots__ + ['Entity']


class FieldClasses(NamespaceExtension):
    """A namespace of field classes."""
    __module__ = __name__
    __slots__ = NamespaceExtension.__slots__


class FieldConstructors(NamespaceExtension):
    """A namespace of field constructor factories."""
    __module__ = __name__
    __slots__ = NamespaceExtension.__slots__


class QueryClasses(NamespaceExtension):
    """A namespace of query classes."""
    __module__ = __name__
    __slots__ = NamespaceExtension.__slots__


class TransactionClasses(NamespaceExtension):
    """A namespace of transaction classes."""
    __module__ = __name__
    __slots__ = NamespaceExtension.__slots__


class ViewClasses(NamespaceExtension):
    """A namespace of view classes."""
    __module__ = __name__
    __slots__ = NamespaceExtension.__slots__


optimize.bind_all(sys.modules[__name__])