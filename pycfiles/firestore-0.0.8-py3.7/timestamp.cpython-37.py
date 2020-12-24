# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/firestore/datatypes/timestamp.py
# Compiled at: 2019-08-25 22:19:11
# Size of source mod 2**32: 2763 bytes
from datetime import datetime, timezone, timedelta
from iso8601 import parse_date, ParseError
from firestore.errors import ValidationError
from firestore.datatypes.base import Base

class Timestamp(Base):
    __doc__ = '\n    Firestore timestamp object. When stored in Cloud Firestore, precise\n    only to microseconds; any additional precision is rounded down\n    '
    __slots__ = ('value', '_name', 'minimum', 'maximum', 'coerce', 'py_type')

    def __init__(self, *args, **kwargs):
        self.minimum = kwargs.get('minimum')
        self.maximum = kwargs.get('maximum')
        self.py_type = datetime
        (super(Timestamp, self).__init__)(*args, **kwargs)

    def do_coercion(self, value):
        """
        Coerce the value provided into the correct underlying type
        for persistence to cloud firestore
        """
        if isinstance(value, int) or isinstance(value, float):
            return datetime.fromtimestamp(float(value)).astimezone()
        return parse_date(value)

    def validate(self, value, instance=None):
        if not isinstance(value, datetime):
            try:
                _val = self.do_coercion(value)
            except:
                raise ValueError(f"Could not load {value} into {self._name}")

        else:
            _val = value
        min_max_msg = '{} field option must be datetime or coercible to datetime'
        if self.minimum and not isinstance(self.minimum, datetime):
            try:
                _min = self.do_coercion(self.minimum)
            except:
                raise ValueError(min_max_msg.format('Minimum'))

        elif _val < _min:
            raise ValidationError(f"Date must be greater than {self.maximum}")
        elif self.maximum and not isinstance(self.maximum, datetime):
            try:
                _max = self.do_coercion(self.maximum)
            except:
                raise ValueError(min_max_msg.format('Maximum'))

            if _val > _max:
                raise ValidationError(f"Date must be greater than {self.maximum}")
        return _val