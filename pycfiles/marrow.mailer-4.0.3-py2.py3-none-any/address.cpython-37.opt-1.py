# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /marrow/mailer/address.py
# Compiled at: 2019-09-13 21:23:39
# Size of source mod 2**32: 6124 bytes
"""TurboMail utility functions and support classes."""
from __future__ import unicode_literals
import sys
from email.utils import formataddr, parseaddr
from email.header import Header
from marrow.mailer.validator import EmailValidator
from marrow.util.compat import basestring, unicode, unicodestr, native
__all__ = [
 'Address', 'AddressList']

class Address(object):
    __doc__ = "Validated electronic mail address class.\n\n\tThis class knows how to validate and format e-mail addresses.  It uses\n\tPython's built-in `parseaddr` and `formataddr` helper functions and helps\n\tguarantee a uniform base for all e-mail address operations.\n\n\tThe AddressList unit tests provide comprehensive testing of this class as\n\twell."

    def __init__(self, name_or_email, email=None, encoding='utf-8'):
        self.encoding = encoding
        if email is None:
            if isinstance(name_or_email, AddressList):
                if not 0 < len(name_or_email) < 2:
                    raise ValueError('AddressList to convert must only contain a single Address.')
                name_or_email = unicode(name_or_email[0])
            if isinstance(name_or_email, (tuple, list)):
                self.name = unicodestr(name_or_email[0], encoding)
                self.address = unicodestr(name_or_email[1], encoding)
            elif isinstance(name_or_email, bytes):
                self.name, self.address = parseaddr(unicodestr(name_or_email, encoding))
            elif isinstance(name_or_email, unicode):
                self.name, self.address = parseaddr(name_or_email)
            else:
                raise TypeError('Expected string, tuple or list, got {0} instead'.format(repr(type(name_or_email))))
        else:
            self.name = unicodestr(name_or_email, encoding)
            self.address = unicodestr(email, encoding)
        email, err = EmailValidator().validate_email(self.address)
        if err:
            raise ValueError('"{0}" is not a valid e-mail address: {1}'.format(email, err))

    def __eq__(self, other):
        if isinstance(other, Address):
            return (
             self.name, self.address) == (other.name, other.address)
        if isinstance(other, unicode):
            return unicode(self) == other
        if isinstance(other, bytes):
            return bytes(self) == other
        if isinstance(other, tuple):
            return (
             self.name, self.address) == other
        raise NotImplementedError('Can not compare Address instance against {0} instance'.format(type(other)))

    def __ne__(self, other):
        return not self == other

    def __len__(self):
        return len(self.__unicode__())

    def __repr__(self):
        return 'Address("{0}")'.format(unicode(self).encode('ascii', 'backslashreplace').decode('ascii'))

    def __unicode__(self):
        return self.encode('utf8').decode('utf8')

    def __bytes__(self):
        return self.encode()

    if sys.version_info < (3, 0):
        __str__ = __bytes__
    else:
        __str__ = __unicode__

    def encode(self, encoding=None):
        name_string = None
        if encoding is None:
            encoding = self.encoding
        elif encoding != 'ascii':
            try:
                self.name.encode('ascii', errors='strict')
            except UnicodeError:
                pass
            else:
                name_string = self.name
        if name_string is None:
            name_string = Header(self.name, encoding).encode()
        localpart, domain = self.address.split('@', 1)
        domain = domain.encode('idna').decode()
        address = '@'.join((localpart, domain))
        return formataddr((name_string, address)).replace('\n', '').encode(encoding)

    @property
    def valid(self):
        email, err = EmailValidator().validate_email(self.address)
        if err:
            return False
        return True


class AddressList(list):

    def __init__(self, addresses=None, encoding='utf-8'):
        super(AddressList, self).__init__()
        self.encoding = encoding
        if addresses is None:
            return
        if isinstance(addresses, basestring):
            addresses = addresses.split(',')
        else:
            if isinstance(addresses, tuple):
                self.append(Address(addresses, encoding=encoding))
                return
            else:
                assert isinstance(addresses, list), 'Invalid value for AddressList: {0}'.format(repr(addresses))
            self.extend(addresses)

    def __repr__(self):
        if not self:
            return 'AddressList()'
        return 'AddressList("{0}")'.format(', '.join([str(i) for i in self]))

    def __bytes__(self):
        return self.encode()

    def __unicode__(self):
        return ', '.join((unicode(i) for i in self))

    if sys.version_info < (3, 0):
        __str__ = __bytes__
    else:
        __str__ = __unicode__

    def __setitem__(self, k, value):
        if isinstance(k, slice):
            value = [Address(val) if not isinstance(val, Address) else val for val in value]
        else:
            if not isinstance(value, Address):
                value = Address(value)
        super(AddressList, self).__setitem__(k, value)

    def __setslice__(self, i, j, sequence):
        self.__setitem__(slice(i, j), sequence)

    def encode(self, encoding=None):
        encoding = encoding if encoding else self.encoding
        return (b', ').join([a.encode(encoding) for a in self])

    def extend(self, sequence):
        values = [Address(val) if not isinstance(val, Address) else val for val in sequence]
        super(AddressList, self).extend(values)

    def append(self, value):
        self.extend([value])

    @property
    def addresses(self):
        return AddressList([i.address for i in self])

    @property
    def string_addresses(self, encoding=None):
        """Return a list of string representations of the addresses suitable
                for usage in an SMTP transaction."""
        if not encoding:
            encoding = self.encoding
        return [Address(i.address).encode(encoding).decode(encoding) for i in self]


class AutoConverter(object):
    __doc__ = 'Automatically converts an assigned value to the given type.'

    def __init__(self, attr, cls, can=True):
        self.cls = cls
        self.can = can
        self.attr = native(attr)

    def __get__(self, instance, owner):
        value = getattr(instance, self.attr, None)
        if value is None:
            if self.can:
                return self.cls()
            return
        return value

    def __set__(self, instance, value):
        if not isinstance(value, self.cls):
            value = self.cls(value)
        setattr(instance, self.attr, value)

    def __delete__(self, instance):
        setattr(instance, self.attr, None)