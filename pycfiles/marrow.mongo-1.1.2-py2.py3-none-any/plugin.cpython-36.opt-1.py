# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /marrow/mongo/core/field/plugin.py
# Compiled at: 2017-09-13 15:15:35
# Size of source mod 2**32: 2304 bytes
from __future__ import unicode_literals
from pkg_resources import iter_entry_points
from ....package.canonical import name as canon
from ....package.loader import load
from ....schema import Attribute
from ....schema.compat import str, unicode
from .base import Field

class PluginReference(Field):
    __doc__ = 'A Python object reference.\n\t\n\tGenerally, for safety sake, you want this to come from a list of available plugins in a given namespace. If a\n\tnamespace is given, the default for `explicit` will be `False`.  If `explicit` is `True` (or no namespace is\n\tdefined) object assignments and literal paths will be allowed.\n\t'
    namespace = Attribute(default=None)
    explicit = Attribute()
    mapping = Attribute(default=None)
    __foreign__ = {
     'string'}

    def __init__(self, *args, **kw):
        if args:
            kw['namespace'] = args[0]
            args = args[1:]
        (super(PluginReference, self).__init__)(*args, **kw)

    def to_native(self, obj, name, value):
        """Transform the MongoDB value into a Marrow Mongo value."""
        if self.mapping:
            for original, new in self.mapping.items():
                value = value.replace(original, new)

        return load(value, self.namespace)

    def to_foreign(self, obj, name, value):
        """Transform to a MongoDB-safe value."""
        namespace = self.namespace
        try:
            explicit = self.explicit
        except AttributeError:
            explicit = not namespace

        if not isinstance(value, (str, unicode)):
            value = canon(value)
        if namespace:
            if ':' in value:
                for point in iter_entry_points(namespace):
                    qualname = point.module_name
                    if point.attrs:
                        qualname += ':' + '.'.join(point.attrs)
                    elif qualname == value:
                        value = point.name
                        break

        if ':' in value:
            if not explicit:
                raise ValueError('Explicit object references not allowed.')
            return value
        else:
            if namespace:
                if value not in (i.name for i in iter_entry_points(namespace)):
                    raise ValueError('Unknown plugin "' + value + '" for namespace "' + namespace + '".')
            return value