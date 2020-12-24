# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/salamoia/h2o/mixin.py
# Compiled at: 2007-12-02 16:26:58


class Mixin(object):
    """
    Inheriting from this class allows the subclass to insert itself int the ancestor list of another class
    """
    __module__ = __name__

    @classmethod
    def mixIn(cls, dest):
        if cls not in dest.__bases__:
            dest.__bases__ = tuple(list(dest.__bases__) + [cls])


from salamoia.tests import *
runDocTests()