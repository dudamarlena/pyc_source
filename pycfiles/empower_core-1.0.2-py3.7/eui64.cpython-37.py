# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/empower_core/eui64.py
# Compiled at: 2020-05-10 06:48:35
# Size of source mod 2**32: 6570 bytes
"""EUI64 data format."""
import re
from pymodm.errors import ValidationError
from pymodm.base.fields import MongoBaseField
from empower_core.serialize import serializable_string
EUI64_PATTERN = re.compile('^([0-9a-fA-F]){2}(:([0-9a-fA-F]){2}){7}$')
PLAIN_PATTERN = re.compile('^([0-9a-fA-F]){16}$')
ID6_PATTERN = re.compile('^([0-9a-fA-F]){1,4}(:([0-9a-fA-F]){1,4}){3}$')

@serializable_string
class EUI64:
    __doc__ = 'EUI64.'
    DEFAULT_VALUE = None
    BYTES = 8

    def __init__(self, data=None):
        """Initialize internal value of EUI64."""
        if data is None:
            self._value = self.DEFAULT_VALUE
        else:
            self._value = self._to_raw_(data)

    @property
    def id6(self):
        """Return data in ID6 format."""
        if self._value == 0:
            return '::0'
        out = '{0:#0{1}x}'.format(self._value, self.BYTES * 2 + 2)[2:]
        out = [out[4 * i:4 * i + 4] + ':' for i in range(int(len(out) / 4))]
        out = ''.join(out)[:-1]
        return out

    @property
    def eui64(self):
        """Return data in EUI format."""
        if self._value == 0:
            return '00:00:00:00:00:00:00:00'
        out = '{0:#0{1}x}'.format(self._value, self.BYTES * 2 + 2)[2:]
        out = [out[2 * i:2 * i + 2] + ':' for i in range(int(len(out) / 2))]
        out = ''.join(out)[:-1]
        return out

    @property
    def hex(self):
        """Return EUID in hex str format."""
        return hex(self._value)[2:]

    @classmethod
    def _to_raw_(cls, data):
        """Return the data as internal representation."""
        if isinstance(data, int):
            return data
            if isinstance(data, EUI64):
                return int(data)
        else:
            if isinstance(data, bytes):
                if len(data) == cls.BYTES * 2:
                    return int.from_bytes(data, byteorder='little')
            assert isinstance(data, str), 'Invalid EUID: %r' % data
        data = re.sub(' ', '', data)
        data = re.sub('[.-]', ':', data)
        if EUI64_PATTERN.match(data) or PLAIN_PATTERN.match(data):
            data = re.sub(':', '', data)
            data = [data[i:i + 2] for i in range(0, len(data), 2)]
            return int(data[0], 16) << 56 | int(data[1], 16) << 48 | int(data[2], 16) << 40 | int(data[3], 16) << 32 | int(data[4], 16) << 24 | int(data[5], 16) << 16 | int(data[6], 16) << 8 | int(data[7], 16)
        if data in ('0', '::'):
            data = '0:0:0:0'
        if data.count(':') == 2:
            data = re.sub('^::', '0:0:0:', data)
            data = re.sub('::$', ':0:0:0', data)
            data = re.sub('::', ':0:0:', data)
        else:
            if data.count(':') == 3:
                data = re.sub('^::', '0:0:', data)
                data = re.sub('::$', ':0:0', data)
                data = re.sub('::', ':0:', data)
            if ID6_PATTERN.match(data):
                data = data.split(':')
                return int(data[0], 16) << 48 | int(data[1], 16) << 32 | int(data[2], 16) << 16 | int(data[3], 16)
            raise ValueError('Invalid EUID: %r' % data)

    def __eq__(self, other):
        """Return if two istances are equal."""
        if isinstance(other, EUI64):
            return self._value == int(other)
        return False

    def __ne__(self, other):
        """Return if two istances are not equal."""
        return not self.__eq__(other)

    def __repr__(self):
        """Return a representation of the instance."""
        return self.__class__.__name__ + "('" + self.id6 + "')"

    def __bool__(self):
        """Return the bool value."""
        return bool(self._value)

    def __hash__(self):
        """Return a hash value."""
        return hash(self._value)

    def __bytes__(self, byteorder='little'):
        """Return EUID in bytes format."""
        byteorder = 'little'
        return self._value.to_bytes(8, byteorder)

    def __str__(self):
        """Return EUID in string format."""
        return self.id6

    def __int__(self):
        """Return EUID in int format."""
        return self._value


class EUI64Field(MongoBaseField):
    __doc__ = 'A field that stores WS URIs.\n\n    This field only accepts EUID64 or ID6 str.\n    '

    def __init__(self, verbose_name=None, mongo_name=None, **kwargs):
        """Init EUID data.

        :parameters:
          - "verbose_name": A human-readable name for the Field.
          - "mongo_name": The name of this field when stored in MongoDB.
        """
        (super().__init__)(verbose_name=verbose_name, mongo_name=mongo_name, **kwargs)

    @classmethod
    def validate(cls, value):
        """Convert value in id6 format."""
        if isinstance(value, EUI64):
            return value.id6
        return EUI64(value).id6

    @classmethod
    def to_mongo(cls, value):
        """Convert EUI64 to a value to be stored in mongodb."""
        if isinstance(value, EUI64):
            return value.id6
        try:
            return EUI64(value).id6
        except ValueError:
            msg = '%r is not a valid EUID.' % value
            raise ValidationError(msg)

    @classmethod
    def to_python(cls, value):
        """Convert a value stored in mongodb to EUI64."""
        try:
            return EUI64(value)
        except ValidationError:
            return value