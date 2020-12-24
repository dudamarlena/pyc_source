# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/spirol/errors.py
# Compiled at: 2015-01-09 08:15:17


class InputFormatError(Exception):
    """
    The input array over which the spirol is iterating is not a pure two dimensional array.
        ie: the number of elements in the input array is not equal to the sum of the array dimensions.
    """
    pass


class UnknownImplementation(ValueError):
    pass


class InvalidDirection(ValueError):
    pass


class InvalidCorner(ValueError):
    pass


class NotSupportedError(Exception):
    pass


class NonSpirolInterface(TypeError):
    pass


if __name__ == '__main__':
    pass