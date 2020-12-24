# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/canossa/exception.py
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