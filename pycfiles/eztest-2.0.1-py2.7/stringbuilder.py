# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\eztest\stringbuilder.py
# Compiled at: 2018-06-29 17:47:45
"""As we known, String is an immutable type. That is, each operation that appears to     modify a String object actually creates a new string.
Although the StringBuilder class generally offers better performance than the String class,     you should not automatically replace String with StringBuilder whenever you want to manipulate strings.     Performance depends on the size of the string, the amount of memory to be allocated for the new string,     the system on which your app is executing, and the type of operation.     You should be prepared to test your app to determine whether StringBuilder actually offers     a significant performance improvement.
"""
from .utility import tostr

class StringBuilder(object):
    __slots__ = [
     'length', 'data']

    def __init__(self, value=None):
        """Initializes a new instance of the StringBuilder class.

        :param str|StringBuilder value: value can be StringBuilder object, or string, or None.
        """
        self.length = 0
        if value is None:
            self.data = []
        elif issubclass(type(value), StringBuilder):
            self.data = value.data
            self.length = value.length
        else:
            value = tostr(value)
            self.data = [value]
            self.length = len(value)
        return

    def append(self, value):
        """Append a string.

        :param str value: value to be appended, will convert to string
        """
        if value is not None:
            value = tostr(value)
            self.data.append(value)
            self.length += len(value)
        return

    def append_line(self, value=None):
        """Append a string with "
".

        :param str value: value to be appended, will convert to string
        """
        if value is None:
            self.data.append('\n')
            self.length += 1
        else:
            value = tostr(value)
            self.data.append(value + '\n')
            self.length += len(value) + 1
        return

    def to_string(self, delimiter=None):
        """Get string from StringBuilder object.

        :param str delimiter : union all members in StringBuilder with delimiter.
        """
        if self.length > 0:
            if delimiter is None:
                return ('').join(self.data)
            return tostr(delimiter).join(self.data)
        else:
            return ''
            return

    def __str__(self):
        """Get string from StringBuilder object."""
        return self.to_string()

    def __len__(self):
        """Get length of StringBuilder object.

        :return int: length of data in StringBuilder.
        """
        return self.length

    def __add__(self, value):
        """Add a string or StringBuilder object.

        :param str|StringBuilder value: value can be StringBuilder object, or string.
        :return StringBuilder: StringBuilder object.
        """
        if isinstance(value, StringBuilder):
            self.data.extend(value.data)
            self.length += value.length
        else:
            self.append(value)
        return self

    def __iadd__(self, other):
        """Add a string or StringBuilder object.

        :param str|StringBuilder other: can be StringBuilder object, or string.
        :return StringBuilder: StringBuilder object.
        """
        return self.__add__(other)