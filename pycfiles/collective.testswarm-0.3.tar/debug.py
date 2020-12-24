# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.darwin-8.9.1-i386/egg/collective/testing/debug.py
# Compiled at: 2007-04-24 16:05:57
import pdb

class Bag(object):
    __module__ = __name__

    def __init__(self, **kw):
        self.__dict__.update(kw)

    update = __init__

    def __repr__(self):
        return '%s' % self.__dict__


_test = False

def dfunc(*args, **kwargs):
    """
    convenience decorator for applying pdb and postmortem

    Test reference integrity(assume use of only)

    >>> func = dfunc(test_func)
    >>> func()
    (<function <lambda> at ...>, True, False)

    >>> func = dfunc(trace=True, pm=True)(test_func)
    >>> func()
    (<function <lambda> at ...>, True, True)
    """
    f = None
    if args and callable(args[0]):
        f = args[0]
    opts = Bag(trace=True, pm=False, func=f, test=_test)
    opts.update(**kwargs)

    def wrap(*args, **kwargs):
        try:
            if opts.trace:
                pdb.set_trace()
            return opts.func(*args, **kwargs)
        except Exception, e:
            if not opts.pm:
                raise e
            else:
                import sys
                pdb.post_mortem(sys.exc_info()[2])

    def mkfunc(func):
        opts.func = func
        return wrap

    if opts.test:

        def wraptest(*args, **kwargs):
            return (opts.func, opts.trace, opts.pm)

        wrap = wraptest
    if opts.func:
        return wrap
    else:
        return mkfunc
    return


def autopsy(func):

    def razor(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except:
            import sys
            pdb.post_mortem(sys.exc_info()[2])

    return razor