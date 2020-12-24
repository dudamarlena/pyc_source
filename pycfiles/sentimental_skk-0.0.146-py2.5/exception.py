# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/sskk/canossa/canossa/exception.py
# Compiled at: 2014-04-25 02:25:23


class CanossaRangeException(Exception):
    """ thrown when an invalid range is detected """

    def __init__(self, message):
        """
        >>> e = CanossaRangeException("test1")
        >>> e.message
        'test1'
        """
        self.message = message

    def __str__(self):
        """
        >>> e = CanossaRangeException("test2")
        >>> e.message
        'test2'
        """
        return repr(self.message)


def test():
    import doctest
    doctest.testmod()


if __name__ == '__main__':
    test()