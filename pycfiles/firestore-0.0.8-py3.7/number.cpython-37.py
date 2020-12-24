# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/firestore/datatypes/number.py
# Compiled at: 2019-08-25 22:19:11
# Size of source mod 2**32: 2708 bytes
from firestore.errors import ValidationError
from firestore.datatypes.base import Base

class Number(Base):
    __doc__ = '\n    Parent of numeric firestore types for method reuse only\n    '
    __slots__ = ('minimum', 'maximum', 'required', 'value', 'pk', '_name', 'coerce',
                 'py_type')

    def __init__(self, *args, **kwargs):
        self.minimum = kwargs.get('minimum')
        self.maximum = kwargs.get('maximum')
        self.required = kwargs.get('required')
        self.pk = kwargs.get('pk')
        self.coerce = kwargs.get('coerce', False)
        (super(Number, self).__init__)(self, *args, **kwargs)

    def validate(self, value, instance=None):
        """
        Run validation of numeric constraints
        """
        if not isinstance(value, (int, float)):
            raise ValueError(f"Non numeric type detected for field {self._name}")
        else:
            if self.__class__.__name__ is 'Integer':
                if isinstance(value, float):
                    if self.coerce:
                        return int(value)
                if isinstance(value, float):
                    raise ValueError(f"Coercing float {self._name} to int might cause precision, explicitly set coerce to true")
            else:
                if self.__class__.__name__ is 'Float':
                    if isinstance(value, int):
                        return float(value)
                if self.minimum and value < self.minimum:
                    raise ValidationError(f"{self._name} has value lower than minimum constraint")
            if self.maximum and value > self.maximum:
                raise ValidationError(f"{self._name} has value higher than maximum constraint")
        return value