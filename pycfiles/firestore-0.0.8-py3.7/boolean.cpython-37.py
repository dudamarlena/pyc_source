# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/firestore/datatypes/boolean.py
# Compiled at: 2019-08-25 22:19:11
# Size of source mod 2**32: 945 bytes
from firestore.errors import ValidationError
from firestore.datatypes.base import Base

class Boolean(Base):
    __doc__ = '\n    Represents a boolean field in the firestore Document instance\n\n    .. py:function:: enumerate(sequence[, start=0])\n\n        Return an iterator that yields tubles of an index and an item of the\n        *sequence*. (And so on.)\n    '
    __slots__ = ('value', 'coerce', '_name', 'py_type')

    def __init__(self, *args, **kwargs):
        self.coerce = kwargs.get('coerce', True)
        self.py_type = bool
        (super(Boolean, self).__init__)(*args, **kwargs)

    def __set_name__(self, instance, name):
        self._name = name

    def validate(self, value, instance=None):
        if self.coerce:
            return bool(value)
        if not isinstance(value, bool):
            raise ValidationError(f"Can not assign non-boolean to {self._name} type boolean")
        return value