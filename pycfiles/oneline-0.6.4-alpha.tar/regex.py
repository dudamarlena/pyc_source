# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: bson/regex.py
# Compiled at: 2014-07-29 17:29:28
"""Tools for representing MongoDB regular expressions.
"""
import re
from bson.son import RE_TYPE
from bson.py3compat import string_types

def str_flags_to_int(str_flags):
    flags = 0
    if 'i' in str_flags:
        flags |= re.IGNORECASE
    if 'l' in str_flags:
        flags |= re.LOCALE
    if 'm' in str_flags:
        flags |= re.MULTILINE
    if 's' in str_flags:
        flags |= re.DOTALL
    if 'u' in str_flags:
        flags |= re.UNICODE
    if 'x' in str_flags:
        flags |= re.VERBOSE
    return flags


class Regex(object):
    """BSON regular expression data."""
    _type_marker = 11

    @classmethod
    def from_native(cls, regex):
        """Convert a Python regular expression into a ``Regex`` instance.

        Note that in Python 3, a regular expression compiled from a
        :class:`str` has the ``re.UNICODE`` flag set. If it is undesirable
        to store this flag in a BSON regular expression, unset it first::

          >>> pattern = re.compile('.*')
          >>> regex = Regex.from_native(pattern)
          >>> regex.flags ^= re.UNICODE
          >>> db.collection.insert({'pattern': regex})

        :Parameters:
          - `regex`: A regular expression object from ``re.compile()``.

        .. warning::
           Python regular expressions use a different syntax and different
           set of flags than MongoDB, which uses `PCRE`_. A regular
           expression retrieved from the server may not compile in
           Python, or may match a different set of strings in Python than
           when used in a MongoDB query.

        .. _PCRE: http://www.pcre.org/
        """
        if not isinstance(regex, RE_TYPE):
            raise TypeError('regex must be a compiled regular expression, not %s' % type(regex))
        return Regex(regex.pattern, regex.flags)

    def __init__(self, pattern, flags=0):
        """BSON regular expression data.

        This class is useful to store and retrieve regular expressions that are
        incompatible with Python's regular expression dialect.

        :Parameters:
          - `pattern`: string
          - `flags`: (optional) an integer bitmask, or a string of flag
            characters like "im" for IGNORECASE and MULTILINE
        """
        if not isinstance(pattern, string_types):
            raise TypeError('pattern must be a string, not %s' % type(pattern))
        self.pattern = pattern
        if isinstance(flags, string_types):
            self.flags = str_flags_to_int(flags)
        elif isinstance(flags, int):
            self.flags = flags
        else:
            raise TypeError('flags must be a string or int, not %s' % type(flags))

    def __eq__(self, other):
        if isinstance(other, Regex):
            return self.pattern == self.pattern and self.flags == other.flags
        else:
            return NotImplemented

    def __ne__(self, other):
        return not self == other

    def __repr__(self):
        return 'Regex(%r, %r)' % (self.pattern, self.flags)

    def try_compile(self):
        """Compile this :class:`Regex` as a Python regular expression.

        .. warning::
           Python regular expressions use a different syntax and different
           set of flags than MongoDB, which uses `PCRE`_. A regular
           expression retrieved from the server may not compile in
           Python, or may match a different set of strings in Python than
           when used in a MongoDB query. :meth:`try_compile()` may raise
           :exc:`re.error`.

        .. _PCRE: http://www.pcre.org/
        """
        return re.compile(self.pattern, self.flags)