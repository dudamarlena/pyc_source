# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/empower_core/etheraddress.py
# Compiled at: 2020-05-10 06:48:36
# Size of source mod 2**32: 5813 bytes
"""Ethernet address."""
from pymodm.errors import ValidationError
from pymodm.base.fields import MongoBaseField
from empower_core.serialize import serializable_string

@serializable_string
class EtherAddress:
    __doc__ = 'Ethernet address.'

    def __init__(self, addr=None):
        if not addr:
            addr = '00:00:00:00:00:00'
        elif isinstance(addr, bytes) and len(addr) == 6:
            self._value = addr
        else:
            if isinstance(addr, str):
                if len(addr) == 17 or addr.count(':') == 5:
                    if len(addr) == 17:
                        if addr[2::3] != ':::::':
                            if addr[2::3] != '-----':
                                raise ValueError('Bad format for ethernet address')
                        addr = ''.join((addr[x * 3:x * 3 + 2] for x in range(0, 6)))
                    else:
                        addr = ''.join(['%02x' % (int(x, 16),) for x in addr.split(':')])
                    addr = (b'').join((bytes((int(addr[x * 2:x * 2 + 2], 16),)) for x in range(0, 6)))
                else:
                    raise ValueError('Expected 6 raw bytes or some hex')
                self._value = addr
            else:
                if isinstance(addr, EtherAddress):
                    self._value = addr.to_raw()
                else:
                    if addr is None:
                        self._value = b'\x00\x00\x00\x00\x00\x00'
                    else:
                        raise ValueError('EtherAddress must be a string of 6 raw bytes')

    def is_global(self):
        """Returns True if this is a globally unique (OUI enforced) address."""
        return not self.is_local()

    def is_local(self):
        """Returns True if this is a locally-administered address."""
        return bool(self._value[0] & 2)

    def is_multicast(self):
        """Returns True if this is a multicast address."""
        return bool(self._value[0] & 1)

    def to_raw(self):
        """Returns the address as a 6-long bytes object."""
        return self._value

    def to_str(self, separator=':'):
        """Return an ASCII representation of the object."""
        return separator.join(('%02x' % (x,) for x in self._value)).upper()

    def match(self, other):
        """ Bitwise match. """
        if isinstance(other, EtherAddress):
            other = other.to_raw()
        else:
            if isinstance(other, bytes):
                pass
            else:
                try:
                    other = EtherAddress(other).to_raw()
                except ValueError:
                    return False

                for cnt in range(0, 6):
                    if self._value[cnt] & other[cnt] != self._value[cnt]:
                        return False

                return True

    def __str__(self):
        return self.to_str()

    def __eq__(self, other):
        if isinstance(other, EtherAddress):
            other = other.to_raw()
        else:
            if isinstance(other, bytes):
                pass
            else:
                try:
                    other = EtherAddress(other).to_raw()
                except ValueError:
                    return False

                if self._value == other:
                    return True
                return False

    def __hash__(self):
        return self._value.__hash__()

    def __repr__(self):
        return self.__class__.__name__ + "('" + self.to_str() + "')"

    def __setattr__(self, a, v):
        if hasattr(self, '_value'):
            raise TypeError('This object is immutable')
        object.__setattr__(self, a, v)

    @classmethod
    def bcast(cls):
        """ Return a broadcast address. """
        return EtherAddress('ff:ff:ff:ff:ff:ff')


class EtherAddressField(MongoBaseField):
    __doc__ = 'A field that stores EtherAddresses.'

    def __init__(self, verbose_name=None, mongo_name=None, **kwargs):
        (super(EtherAddressField, self).__init__)(verbose_name=verbose_name, mongo_name=mongo_name, **kwargs)

        def validate_ethernet_address(value):
            try:
                EtherAddress(value)
            except ValueError:
                msg = '%r is not a valid Ethernet address.' % value
                raise ValidationError(msg)

        self.validators.append(validate_ethernet_address)

    @classmethod
    def to_mongo(cls, value):
        """Convert value for storage."""
        try:
            return str(value)
        except ValueError:
            msg = '%r is not a valid Ethernet address.' % value
            raise ValidationError(msg)

    @classmethod
    def to_python(cls, value):
        """Convert value back to Python."""
        try:
            return EtherAddress(value)
        except ValueError:
            msg = '%r is not a valid Ethernet address.' % value
            raise ValidationError(msg)