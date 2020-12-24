# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/lib/python2.7/site-packages/btform/dataform.py
# Compiled at: 2015-09-16 04:15:41
import copy
from btform import attrget
from btform import storage
from btform import AttributeList

class Form(object):

    def __init__(self, *inputs, **kw):
        self.inputs = inputs
        self.valid = True
        self.note = None
        self.validators = kw.pop('validators', [])
        return

    def __call__(self, x=None):
        o = copy.deepcopy(self)
        if x:
            o.validates(x)
        return o

    @property
    def errors(self):
        return (',').join([ '%s error,%s' % (i.description, i.note) for i in self.inputs if i.note ])

    def validates(self, source=None, _validate=True, **kw):
        source = source or kw
        out = True
        for i in self.inputs:
            v = attrget(source, i.name)
            if _validate:
                out = i.validate(v) and out
            else:
                i.set_value(v)

        if _validate:
            out = out and self._validate(source)
            self.valid = out
        return out

    def _validate(self, value):
        self.value = value
        for v in self.validators:
            if not v.valid(value):
                self.note = v.msg
                return False

        return True

    def fill(self, source=None, **kw):
        return self.validates(source, _validate=False, **kw)

    def __getitem__(self, i):
        for x in self.inputs:
            if x.name == i:
                return x

        raise KeyError, i

    def __getattr__(self, name):
        inputs = self.__dict__.get('inputs') or []
        for x in inputs:
            if x.name == name:
                return x

        raise AttributeError, name

    def get(self, i, default=None):
        try:
            return self[i]
        except KeyError:
            return default

    def _get_d(self):
        return storage([ (i.name, i.get_value()) for i in self.inputs ])

    d = property(_get_d)


class Item(object):

    def __init__(self, name, *validators, **attrs):
        self.name = name
        self.validators = validators
        self.attrs = attrs = AttributeList(attrs)
        self.description = attrs.pop('description', name)
        self.value = attrs.pop('value', None)
        self.note = None
        self.id = attrs.setdefault('id', self.get_default_id())
        return

    def get_default_id(self):
        return self.name

    def validate(self, value):
        self.set_value(value)
        for v in self.validators:
            if not v.valid(value):
                self.note = v.msg
                return False

        return True

    def set_value(self, value):
        self.value = value

    def get_value(self):
        return self.value

    def addatts(self):
        return ' ' + str(self.attrs)