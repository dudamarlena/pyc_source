# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/firestore/datatypes/string.py
# Compiled at: 2019-08-25 22:19:11
# Size of source mod 2**32: 1819 bytes
from firestore.errors import ValidationError
from firestore.datatypes.base import Base

class String(Base):
    __slots__ = ('minimum', 'maximum', 'coerce', '_name', 'value', 'py_type')

    def __init__(self, *args, **kwargs):
        self.minimum = kwargs.get('minimum')
        self.maximum = kwargs.get('maximum')
        self.coerce = kwargs.get('coerce', True)
        self.py_type = str
        (super(String, self).__init__)(*args, **kwargs)

    def validate(self, value, instance=None):
        if not isinstance(value, str):
            if not self.coerce:
                raise ValueError(f"Can not assign type {type(value)} to str and coerce is disabled")
            value = str(value)
        else:
            max_msg = f"{self._name} must have a maximum len of {self.maximum}, found {len(value)}"
            min_msg = f"{self._name} must have minimum len of {self.minimum}, found {len(value)}"
            if self.minimum:
                if self.minimum > len(value):
                    raise ValidationError(min_msg)
            if self.maximum:
                if self.maximum < len(value):
                    raise ValidationError(max_msg)
            if self.required:
                if not value:
                    raise ValidationError(f"{self._name} is a required field")
            if self.options and value not in self.options:
                raise ValidationError(f"Value {value} not found in options {self.options}")
        if isinstance(value, str):
            return value
        if self.coerce:
            if isinstance(value, (int, float)):
                return str(value)
            raise ValueError(f"Can not coerce {type(value)} to str")
        raise ValueError(f"{value} is not of type str and coerce is {self.coerce}")