# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.5/site-packages/future/types/newbytes.py
# Compiled at: 2016-10-27 16:05:38
# Size of source mod 2**32: 15351 bytes
"""
Pure-Python implementation of a Python 3-like bytes object for Python 2.

Why do this? Without it, the Python 2 bytes object is a very, very
different beast to the Python 3 bytes object.
"""
from collections import Iterable
from numbers import Integral
import string, copy
from future.utils import istext, isbytes, PY3, with_metaclass
from future.types import no, issubset
from future.types.newobject import newobject
_builtin_bytes = bytes
if PY3:
    unicode = str

class BaseNewBytes(type):

    def __instancecheck__(cls, instance):
        if cls == newbytes:
            return isinstance(instance, _builtin_bytes)
        else:
            return issubclass(instance.__class__, cls)


def _newchr(x):
    if isinstance(x, str):
        return x.encode('ascii')
    else:
        return chr(x)


class newbytes(with_metaclass(BaseNewBytes, _builtin_bytes)):
    __doc__ = '\n    A backport of the Python 3 bytes object to Py2\n    '

    def __new__(cls, *args, **kwargs):
        """
        From the Py3 bytes docstring:

        bytes(iterable_of_ints) -> bytes
        bytes(string, encoding[, errors]) -> bytes
        bytes(bytes_or_buffer) -> immutable copy of bytes_or_buffer
        bytes(int) -> bytes object of size given by the parameter initialized with null bytes
        bytes() -> empty bytes object

        Construct an immutable array of bytes from:
          - an iterable yielding integers in range(256)
          - a text string encoded using the specified encoding
          - any object implementing the buffer API.
          - an integer
        """
        encoding = None
        errors = None
        if len(args) == 0:
            return super(newbytes, cls).__new__(cls)
        else:
            if len(args) >= 2:
                args = list(args)
                if len(args) == 3:
                    errors = args.pop()
                encoding = args.pop()
            if type(args[0]) == newbytes:
                return args[0]
            if isinstance(args[0], _builtin_bytes):
                value = args[0]
            else:
                if isinstance(args[0], unicode):
                    try:
                        if 'encoding' in kwargs:
                            assert encoding is None
                            encoding = kwargs['encoding']
                        if 'errors' in kwargs:
                            assert errors is None
                            errors = kwargs['errors']
                    except AssertionError:
                        raise TypeError('Argument given by name and position')

                    if encoding is None:
                        raise TypeError('unicode string argument without an encoding')
                    newargs = [
                     encoding]
                    if errors is not None:
                        newargs.append(errors)
                    value = args[0].encode(*newargs)
                else:
                    if isinstance(args[0], Iterable):
                        if len(args[0]) == 0:
                            value = b''
                        else:
                            try:
                                value = bytearray([_newchr(x) for x in args[0]])
                            except:
                                raise ValueError('bytes must be in range(0, 256)')

                    else:
                        if isinstance(args[0], Integral):
                            if args[0] < 0:
                                raise ValueError('negative count')
                            value = b'\x00' * args[0]
                        else:
                            value = args[0]
                if type(value) == newbytes:
                    return copy.copy(value)
            return super(newbytes, cls).__new__(cls, value)

    def __repr__(self):
        return 'b' + super(newbytes, self).__repr__()

    def __str__(self):
        return 'b' + "'{0}'".format(super(newbytes, self).__str__())

    def __getitem__(self, y):
        value = super(newbytes, self).__getitem__(y)
        if isinstance(y, Integral):
            return ord(value)
        else:
            return newbytes(value)

    def __getslice__(self, *args):
        return self.__getitem__(slice(*args))

    def __contains__(self, key):
        if isinstance(key, int):
            newbyteskey = newbytes([key])
        else:
            if type(key) == newbytes:
                newbyteskey = key
            else:
                newbyteskey = newbytes(key)
        return issubset(list(newbyteskey), list(self))

    @no(unicode)
    def __add__(self, other):
        return newbytes(super(newbytes, self).__add__(other))

    @no(unicode)
    def __radd__(self, left):
        return newbytes(left) + self

    @no(unicode)
    def __mul__(self, other):
        return newbytes(super(newbytes, self).__mul__(other))

    @no(unicode)
    def __rmul__(self, other):
        return newbytes(super(newbytes, self).__rmul__(other))

    def join(self, iterable_of_bytes):
        errmsg = 'sequence item {0}: expected bytes, {1} found'
        if isbytes(iterable_of_bytes) or istext(iterable_of_bytes):
            raise TypeError(errmsg.format(0, type(iterable_of_bytes)))
        for i, item in enumerate(iterable_of_bytes):
            if istext(item):
                raise TypeError(errmsg.format(i, type(item)))

        return newbytes(super(newbytes, self).join(iterable_of_bytes))

    @classmethod
    def fromhex(cls, string):
        return cls(string.replace(' ', '').decode('hex'))

    @no(unicode)
    def find(self, sub, *args):
        return super(newbytes, self).find(sub, *args)

    @no(unicode)
    def rfind(self, sub, *args):
        return super(newbytes, self).rfind(sub, *args)

    @no(unicode, (1, 2))
    def replace(self, old, new, *args):
        return newbytes(super(newbytes, self).replace(old, new, *args))

    def encode(self, *args):
        raise AttributeError('encode method has been disabled in newbytes')

    def decode(self, encoding='utf-8', errors='strict'):
        """
        Returns a newstr (i.e. unicode subclass)

        Decode B using the codec registered for encoding. Default encoding
        is 'utf-8'. errors may be given to set a different error
        handling scheme.  Default is 'strict' meaning that encoding errors raise
        a UnicodeDecodeError.  Other possible values are 'ignore' and 'replace'
        as well as any other name registered with codecs.register_error that is
        able to handle UnicodeDecodeErrors.
        """
        from future.types.newstr import newstr
        if errors == 'surrogateescape':
            from future.utils.surrogateescape import register_surrogateescape
            register_surrogateescape()
        return newstr(super(newbytes, self).decode(encoding, errors))

    @no(unicode)
    def startswith(self, prefix, *args):
        return super(newbytes, self).startswith(prefix, *args)

    @no(unicode)
    def endswith(self, prefix, *args):
        return super(newbytes, self).endswith(prefix, *args)

    @no(unicode)
    def split(self, sep=None, maxsplit=-1):
        parts = super(newbytes, self).split(sep, maxsplit)
        return [newbytes(part) for part in parts]

    def splitlines(self, keepends=False):
        """
        B.splitlines([keepends]) -> list of lines

        Return a list of the lines in B, breaking at line boundaries.
        Line breaks are not included in the resulting list unless keepends
        is given and true.
        """
        parts = super(newbytes, self).splitlines(keepends)
        return [newbytes(part) for part in parts]

    @no(unicode)
    def rsplit(self, sep=None, maxsplit=-1):
        parts = super(newbytes, self).rsplit(sep, maxsplit)
        return [newbytes(part) for part in parts]

    @no(unicode)
    def partition(self, sep):
        parts = super(newbytes, self).partition(sep)
        return tuple(newbytes(part) for part in parts)

    @no(unicode)
    def rpartition(self, sep):
        parts = super(newbytes, self).rpartition(sep)
        return tuple(newbytes(part) for part in parts)

    @no(unicode, (1, ))
    def rindex(self, sub, *args):
        """
        S.rindex(sub [,start [,end]]) -> int

        Like S.rfind() but raise ValueError when the substring is not found.
        """
        pos = self.rfind(sub, *args)
        if pos == -1:
            raise ValueError('substring not found')

    @no(unicode)
    def index(self, sub, *args):
        """
        Returns index of sub in bytes.
        Raises ValueError if byte is not in bytes and TypeError if can't
        be converted bytes or its length is not 1.
        """
        if isinstance(sub, int):
            if len(args) == 0:
                start, end = 0, len(self)
        else:
            if len(args) == 1:
                start = args[0]
            else:
                if len(args) == 2:
                    start, end = args
                else:
                    raise TypeError('takes at most 3 arguments')
                return list(self)[start:end].index(sub)
            if not isinstance(sub, bytes):
                try:
                    sub = self.__class__(sub)
                except (TypeError, ValueError):
                    raise TypeError("can't convert sub to bytes")

                try:
                    return super(newbytes, self).index(sub, *args)
                except ValueError:
                    raise ValueError('substring not found')

    def __eq__(self, other):
        if isinstance(other, (_builtin_bytes, bytearray)):
            return super(newbytes, self).__eq__(other)
        else:
            return False

    def __ne__(self, other):
        if isinstance(other, _builtin_bytes):
            return super(newbytes, self).__ne__(other)
        else:
            return True

    unorderable_err = 'unorderable types: bytes() and {0}'

    def __lt__(self, other):
        if not isbytes(other):
            raise TypeError(self.unorderable_err.format(type(other)))
        return super(newbytes, self).__lt__(other)

    def __le__(self, other):
        if not isbytes(other):
            raise TypeError(self.unorderable_err.format(type(other)))
        return super(newbytes, self).__le__(other)

    def __gt__(self, other):
        if not isbytes(other):
            raise TypeError(self.unorderable_err.format(type(other)))
        return super(newbytes, self).__gt__(other)

    def __ge__(self, other):
        if not isbytes(other):
            raise TypeError(self.unorderable_err.format(type(other)))
        return super(newbytes, self).__ge__(other)

    def __native__(self):
        return super(newbytes, self).__str__()

    def __getattribute__(self, name):
        """
        A trick to cause the ``hasattr`` builtin-fn to return False for
        the 'encode' method on Py2.
        """
        if name in ('encode', 'encode'):
            raise AttributeError('encode method has been disabled in newbytes')
        return super(newbytes, self).__getattribute__(name)

    @no(unicode)
    def rstrip(self, bytes_to_strip=None):
        """
        Strip trailing bytes contained in the argument.
        If the argument is omitted, strip trailing ASCII whitespace.
        """
        return newbytes(super(newbytes, self).rstrip(bytes_to_strip))

    @no(unicode)
    def strip(self, bytes_to_strip=None):
        """
        Strip leading and trailing bytes contained in the argument.
        If the argument is omitted, strip trailing ASCII whitespace.
        """
        return newbytes(super(newbytes, self).strip(bytes_to_strip))

    def lower(self):
        """
        b.lower() -> copy of b

        Return a copy of b with all ASCII characters converted to lowercase.
        """
        return newbytes(super(newbytes, self).lower())

    @no(unicode)
    def upper(self):
        """
        b.upper() -> copy of b

        Return a copy of b with all ASCII characters converted to uppercase.
        """
        return newbytes(super(newbytes, self).upper())

    @classmethod
    @no(unicode)
    def maketrans(cls, frm, to):
        """
        B.maketrans(frm, to) -> translation table

        Return a translation table (a bytes object of length 256) suitable
        for use in the bytes or bytearray translate method where each byte
        in frm is mapped to the byte at the same position in to.
        The bytes objects frm and to must be of the same length.
        """
        return newbytes(string.maketrans(frm, to))


__all__ = [
 'newbytes']