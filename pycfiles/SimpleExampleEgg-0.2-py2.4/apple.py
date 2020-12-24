# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/fruit/apple.py
# Compiled at: 2005-12-14 18:33:04
import sys

def doConsole():
    print make_pie('CONSOLE')


def make_pie(who):
    """
>>> import apple as a
>>> a.make_pie('Todd')
'Todd likes pie!!!'
        """
    return '%s likes pie!!!' % who


def _test():
    import doctest
    return doctest.testmod()


if __name__ == '__main__':
    _test()
    if len(sys.argv) > 1:
        print make_pie(sys.argv[1])