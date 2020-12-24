# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/mortar/field.py
# Compiled at: 2008-12-19 12:41:15
from interfaces import IField, IFieldType, empty
from types import text, type as type_of
from zope.interface import implements

class Field:
    implements(IField)

    def __init__(self, content, name):
        self.content = content
        self.name = name

    def __unicode__(self):
        return text(self.content.data.get(self.name))

    def __repr__(self):
        return '<Field %r containing %r>' % (
         self.name,
         self.content.data.get(self.name))

    def get(self, default=None, type=None):
        v = self.content.data.get(self.name)
        if v is None:
            v = default
        if type is not None:
            return type(v)
        else:
            return v

    def set(self, value, type=IFieldType):
        self.content[self.name] = type(value)

    def add(self, value, type=IFieldType):
        value = type(value)
        if value is empty:
            return
        name = self.name
        data = self.content.data
        current = data.get(name)
        if name not in data:
            current = data[name] = []
        elif isinstance(current, basestring):
            current = data[name] = [
             current]
        elif not isinstance(current, list):
            current = data[self.name] = list(current)
        if isinstance(value, (tuple, list)):
            if current and type_of(value) != type_of(current):
                raise TypeError("Can't add %s to %s" % (
                 type_of(value).__name__, type_of(current).__name__))
            self.content.data[self.name].extend(value)
        else:
            if current and type_of(value) != type_of(current[0]):
                raise TypeError("Can't add %s to %s" % (
                 type_of(value).__name__, type_of(current).__name__))
            self.content.data[self.name].append(value)

    @property
    def type(self):
        return type_of(self.content.data.get(self.name))

    def canSet(self, user=None):
        raise NotImplementedError
        return True

    def canGet(self, user=None):
        raise NotImplementedError
        return self.data.has_key(name)

    def delete(self):
        del self.content[self.name]