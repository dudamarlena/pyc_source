# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/fruit/orange.py
# Compiled at: 2005-12-14 15:11:19


def squeeze_me():
    """
>>> import orange as o
>>> o.squeeze_me()
'have some orange juice!'
        """
    return 'have some orange juice!'


def _test():
    import doctest, orange
    return doctest.testmod(orange)


if __name__ == '__main__':
    _test()