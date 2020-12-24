# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/fabrom/workspace/jability-python-package/runtests.py
# Compiled at: 2013-05-25 04:38:30
if __name__ == '__main__':
    import doctest
    doctest.testmod()
    try:
        import nose
        nose.main()
    except ImportError:
        pass