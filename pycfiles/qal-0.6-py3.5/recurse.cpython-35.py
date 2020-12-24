# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/qal/common/recurse.py
# Compiled at: 2016-04-12 13:41:36
# Size of source mod 2**32: 883 bytes
__author__ = 'nibo'

class Recurse(object):
    __doc__ = 'This class provides helper functions for recursion\n    '
    debuglevel = 2
    nestinglevel = 0

    def _print_nestinglevel(self, _value):
        """Prints the current nesting level. Not thread safe."""
        self._debug_print(_value + ' level: ' + str(self.nestinglevel), 4)

    def _get_up(self, _value):
        """Gets up one nesting level. Not thread safe."""
        self.nestinglevel -= 1
        self._print_nestinglevel('Leaving ' + _value)

    def _go_down(self, _value):
        """Gets down one nesting level. Not thread safe."""
        self.nestinglevel += 1
        self._print_nestinglevel('Entering ' + _value)

    def _debug_print(self, _value, _debuglevel=3):
        """Prints a debug message if the debugging level is sufficient."""
        if self.debuglevel >= _debuglevel:
            print(_value)