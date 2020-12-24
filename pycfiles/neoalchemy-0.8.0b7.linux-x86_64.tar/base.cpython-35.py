# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/zuul/projects/neoalchemy/lib/python3.5/site-packages/neoalchemy/schema/base.py
# Compiled at: 2016-07-16 18:14:38
# Size of source mod 2**32: 2936 bytes
from collections import OrderedDict
from itertools import chain
from .operations import OperatorInterface

class Property(OperatorInterface):

    def __init__(self, name=None, type=str, default=None, indexed=False, unique=False, required=False):
        self._Property__name = str(name) if name else None
        self.unique = bool(unique)
        self.indexed = self.unique or bool(indexed)
        self.required = bool(required)
        self.type = type
        self.default = default
        self._Property__value = self.value = None

    @property
    def name(self):
        return self._Property__name

    @name.setter
    def name(self, value):
        if self._Property__name is not None:
            raise AttributeError("Can't change Property name once set.")
        self._Property__name = str(value)

    @property
    def schema(self):
        params = {'label': self.label, 
         'lower_label': self.label.lower(), 
         'name': self._Property__name}
        schema = []
        if self.unique:
            constraint = 'CONSTRAINT ON ( %(lower_label)s:%(label)s ) ASSERT %(lower_label)s.%(name)s IS UNIQUE'
            schema.append(constraint % params)
        elif self.indexed:
            schema.append('INDEX ON :%(label)s(%(name)s)' % params)
        if self.required:
            constraint = 'CONSTRAINT ON ( %(lower_label)s:%(label)s ) ASSERT exists(%(lower_label)s.%(name)s)'
            schema.append(constraint % params)
        return schema

    @property
    def value(self):
        return self._Property__value

    @value.setter
    def value(self, value):
        if value is None:
            value = self.default() if callable(self.default) else self.default
        if value is not None:
            value = self.type(value)
        self._Property__value = value


class NodeType(object):

    def __init__(self, label, *properties, **kw):
        self._NodeType__labels = (
         label,) + tuple(kw.get('extra_labels', ()))
        self._NodeType__properties = OrderedDict()
        for prop in properties:
            if not isinstance(prop, Property):
                raise TypeError("Must be a Property object. '%s' given." % prop.__class__)
            prop.label = label
            if prop.name in self._NodeType__properties:
                raise ValueError("Duplicate property found: '%s'" % prop.name)
            self._NodeType__properties[prop.name] = prop

    @property
    def LABEL(self):
        return self._NodeType__labels[0]

    @property
    def labels(self):
        return self._NodeType__labels

    @property
    def schema(self):
        return [s for p in self._NodeType__properties.values() for s in p.schema]

    @property
    def properties(self):
        return self._NodeType__properties

    def __getattr__(self, attr):
        try:
            return self._NodeType__properties[attr]
        except KeyError:
            super(NodeType, self).__getattribute__(attr)