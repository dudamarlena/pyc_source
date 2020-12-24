# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/firestore/datatypes/base.py
# Compiled at: 2019-08-25 22:19:11
# Size of source mod 2**32: 1462 bytes
from firestore.errors import PKError
PKS = ('integer', 'float', 'string', 'geopoint')

class Base(object):
    __doc__ = '\n    Super class for document valid datatypes\n    '

    def __init__(self, *args, **kwargs):
        self.pk = kwargs.get('pk')
        self.required = kwargs.get('required')
        self.default = kwargs.get('default')
        self.unique = kwargs.get('unique')
        self.textsearch = kwargs.get('textsearch')
        self.options = kwargs.get('options')
        self.value = None

    def __get__(self, instance, metadata):
        return instance.get_field(self)

    def __set__(self, instance, value):
        if self.pk:
            if type(self).__name__.lower() not in PKS:
                raise PKError(f"Fields of type {type(self).__name__} can not be set as primary key")
            instance.pk = self
        if self.unique:
            instance.uniques = (
             self._name, value)
        self.validate(value, instance)
        self.value = value
        instance.__mutated__ = True
        instance.add_field(self, value)

    def __set_name__(self, cls, name):
        self._name = name

    def cast(self, instance, value):
        self.validate(value, instance)
        if isinstance(value, self.py_type):
            return value
        return self.py_type(value)

    def validate(self, value, instance=None):
        pass