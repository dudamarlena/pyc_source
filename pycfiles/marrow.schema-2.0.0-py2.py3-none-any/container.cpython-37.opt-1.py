# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /marrow/schema/transform/container.py
# Compiled at: 2018-12-02 18:39:27
# Size of source mod 2**32: 2203 bytes
from .base import Concern, Transform, Attribute

class Array(Transform):
    __doc__ = 'Convert array-like values.\n\t\n\tIntelligently handles list and non-string values, returning as-is and passing to the list builtin respectively.\n\t\n\tFor a more advanced method of converting between strings and iterables see the Token transformer.\n\t\n\tWith the provided defaults (comma separator, exclusion of empty elements, stripping of whitespace, and casting to\n\ta list) the following example applies::\n\t\n\t\t"foo,bar, baz   , , diz" -> [\'foo\', \'bar\', \'baz\', \'diz\'] -> "foo,bar,baz,diz"\n\t'
    separator = Attribute(default=', ')
    empty = Attribute(default=False)
    cast = Attribute(default=list)

    def _clean(self, value):
        """Perform a standardized pipline of operations across an iterable."""
        value = (str(v) for v in value)
        if self.strip:
            value = (v.strip() for v in value)
        if not self.empty:
            value = (v for v in value if v)
        return value

    def native(self, value, context=None):
        """Convert the given string into a list of substrings."""
        separator = self.separator.strip() if (self.strip and hasattr(self.separator, 'strip')) else (self.separator)
        value = super().native(value, context)
        if value is None:
            return self.cast()
        if hasattr(value, 'split'):
            value = value.split(separator)
        value = self._clean(value)
        try:
            if self.cast:
                return self.cast(value)
            return value
        except Exception as e:
            try:
                raise Concern('{0} caught, failed to perform array transform: {1}', e.__class__.__name__, str(e))
            finally:
                e = None
                del e

    def foreign(self, value, context=None):
        """Construct a string-like representation for an iterable of string-like objects."""
        if self.separator is None:
            separator = ' '
        else:
            separator = self.separator.strip() if (self.strip and hasattr(self.separator, 'strip')) else (self.separator)
        value = self._clean(value)
        try:
            value = separator.join(value)
        except Exception as e:
            try:
                raise Concern('{0} caught, failed to convert to string: {1}', e.__class__.__name__, str(e))
            finally:
                e = None
                del e

        return super().foreign(value)


array = Array()