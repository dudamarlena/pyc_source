# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /marrow/schema/exc.py
# Compiled at: 2018-12-03 10:42:34
# Size of source mod 2**32: 1138 bytes
import sys, copy
from logging import getLevelName, DEBUG, INFO, WARNING, ERROR, CRITICAL

class Concern(Exception):
    __doc__ = 'There was an error validating data.\n\t\n\tOnly `logging.ERROR` (and above) validation concerns should be treated as actual errors.\n\t'

    def __init__(self, level=ERROR, message='Unspecified error.', *args, **kw):
        """Can be instantiated with the message first (and no way to populate a level other than ERROR)."""
        if isinstance(level, int):
            args = (
             level, message) + args
        else:
            args = (
             message,) + args
            message = level
            level = ERROR
        self.message = message
        self.level = level
        self.concerns = kw.pop('concerns', [])
        self.kwargs = kw
        (super().__init__)(*args)

    def __str__(self):
        """Format the validation concern for human consumption.
                
                We have the seemingly pointless wrapping call to str() here to allow for lazy translation.
                """
        return (str(self.message).format)(*self.args, **self.kwargs)

    def __repr__(self):
        result = '{0}({1}, "{2}")'.format(self.__class__.__name__, getLevelName(self.level), str(self).replace('"', '"'))
        return result