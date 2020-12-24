# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\User\AppData\Local\Temp\pip-install-oj_abz_z\hypothesis\hypothesis\internal\lazyformat.py
# Compiled at: 2020-01-12 08:06:33
# Size of source mod 2**32: 1237 bytes


class lazyformat:
    __doc__ = "A format string that isn't evaluated until it's needed."

    def __init__(self, format_string, *args):
        self._lazyformat__format_string = format_string
        self._lazyformat__args = args

    def __str__(self):
        return self._lazyformat__format_string % self._lazyformat__args

    def __eq__(self, other):
        return isinstance(other, lazyformat) and self._lazyformat__format_string == other._lazyformat__format_string and self._lazyformat__args == other._lazyformat__args

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self._lazyformat__format_string)