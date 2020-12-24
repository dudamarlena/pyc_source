# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/empower_core/ssid.py
# Compiled at: 2020-05-10 06:48:32
# Size of source mod 2**32: 3517 bytes
"""Wi-Fi Service Set Identifier (SSID)."""
import re
from pymodm.errors import ValidationError
from pymodm.base.fields import MongoBaseField
from empower_core.serialize import serializable_string
WIFI_NWID_MAXSIZE = 32

@serializable_string
class SSID:
    __doc__ = 'Wi-Fi Service Set Identifier (SSID).'

    def __init__(self, ssid=None):
        if not ssid:
            ssid = ''
        elif isinstance(ssid, bytes):
            self.ssid = ssid.decode('UTF-8').rstrip('\x00')
        else:
            if isinstance(ssid, str):
                allowed = re.compile('^[a-zA-Z0-9 ]*$', re.VERBOSE | re.IGNORECASE)
                if allowed.match(ssid) is None:
                    raise ValueError('Invalid SSID name')
                self.ssid = ssid
            else:
                if isinstance(ssid, SSID):
                    self.ssid = str(ssid)
                else:
                    raise ValueError('SSID must be a string or an array of UTF-8 encoded bytes array of UTF-8 encoded bytes')

    def to_raw(self):
        """ Return the bytes represenation of the SSID """
        bytes_ssid = self.ssid.encode('UTF-8')
        return bytes_ssid + b'\x00' * (WIFI_NWID_MAXSIZE + 1 - len(bytes_ssid))

    def to_str(self):
        """Return an ASCII representation of the object."""
        return self.ssid

    def __bool__(self):
        return bool(self.ssid)

    def __str__(self):
        return self.to_str()

    def __len__(self):
        return len(self.ssid)

    def __hash__(self):
        return hash(self.ssid)

    def __eq__(self, other):
        if isinstance(other, SSID):
            return self.ssid == other.ssid
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return self.__class__.__name__ + "('" + self.to_str() + "')"


class SSIDField(MongoBaseField):
    __doc__ = 'A field that stores SSIDs.'

    def __init__(self, verbose_name=None, mongo_name=None, **kwargs):
        (super(SSIDField, self).__init__)(verbose_name=verbose_name, mongo_name=mongo_name, **kwargs)

        def validate_ssid(value):
            try:
                SSID(value)
            except ValueError:
                msg = '%r is not a valid SSID.' % value
                raise ValidationError(msg)

        self.validators.append(validate_ssid)

    @classmethod
    def to_mongo(cls, value):
        """Convert value for storage."""
        try:
            return str(value)
        except ValueError:
            msg = '%r is not a valid SSID.' % value
            raise ValidationError(msg)

    @classmethod
    def to_python(cls, value):
        """Convert value back to Python."""
        try:
            return SSID(value)
        except ValueError:
            msg = '%r is not a valid SSID.' % value
            raise ValidationError(msg)