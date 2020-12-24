# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.4-x86_64/egg/trachet/iomode.py
# Compiled at: 2014-07-01 10:29:06
import template
_DIRECTION_INPUT = True
_DIRECTION_OUTPUT = False

class IOMode(object):
    """
    >>> mode = IOMode()
    >>> mode.is_input()
    True
    >>> mode.get_prompt() == template.getinputprompt()
    True
    >>> mode.set_output()
    >>> mode.is_output()
    True
    >>> mode.get_prompt() == template.getoutputprompt()
    True
    """
    _direction = _DIRECTION_INPUT

    def is_input(self):
        return self._direction == _DIRECTION_INPUT

    def is_output(self):
        return self._direction == _DIRECTION_OUTPUT

    def set_input(self):
        self._direction = _DIRECTION_INPUT

    def set_output(self):
        self._direction = _DIRECTION_OUTPUT

    def get_prompt(self):
        if self.is_input():
            return template.getinputprompt()
        return template.getoutputprompt()


def _test():
    import doctest
    doctest.testmod()


if __name__ == '__main__':
    _test()