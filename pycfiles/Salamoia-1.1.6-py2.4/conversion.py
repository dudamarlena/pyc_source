# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/salamoia/h2o/decorators/conversion.py
# Compiled at: 2007-12-02 16:26:56


class ConvertArgumentTypes(object):
    """Converts function arguments to specified types."""
    __module__ = __name__

    def __init__(self, *args, **kw):
        self.args = args
        self.kw = kw

    def __call__(self, f):

        def func(*args, **kw):
            nargs = [ x[0](x[1]) for x in zip(self.args, args) ]
            invalidkw = [ x for x in kw if x not in self.kw ]
            if len(invalidkw) > 0:
                raise TypeError, f.func_name + "() got an unexpected keyword argument '%s'" % invalidkw[0]
            kw = dict([ (x, self.kw[x](kw[x])) for x in kw ])
            v = f(*nargs, **kw)
            return v

        return func


from salamoia.tests import *
runDocTests()