# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/salamoia/utility/null.py
# Compiled at: 2007-12-02 16:26:55


class Null:
    """ 
    Null objects always and reliably "do nothing." 

    >>> null = Null()
    >>> null.test.blabla().something() is null
    True

    """
    __module__ = __name__

    def __init__(self, *args, **kwargs):
        pass

    def __call__(self, *args, **kwargs):
        return self

    def __repr__(self):
        return 'Null'

    def __nonzero__(self):
        return 0

    def __getattr__(self, name):
        return self

    def __setattr__(self, name, value):
        return self

    def __delattr__(self, name):
        return self


from salamoia.tests import *
runDocTests()