# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/salamoia/h2o/decorators/exceptionhandler.py
# Compiled at: 2007-12-02 16:26:56
__author__ = 'Anand Pillai'

def ExpHandler(*posargs):

    def nestedhandler(func, exptuple, *pargs, **kwargs):
        """ Function that creates a nested exception handler from
        the passed exception tuple """
        (exp, handler) = exptuple[0]
        try:
            if len(exptuple) == 1:
                func(*pargs, **kwargs)
            else:
                nestedhandler(func, exptuple[1:], *pargs, **kwargs)
        except exp, e:
            if handler:
                handler(e)
            else:
                print e.__class__.__name__, ':', e

    def wrapper(f):

        def newfunc(*pargs, **kwargs):
            if len(posargs) < 2:
                t = tuple((item for item in posargs[0] if issubclass(item, Exception) or (Exception,)))
                try:
                    f(*pargs, **kwargs)
                except t, e:
                    print e.__class__.__name__, ':', e

            else:
                t1, t2 = posargs[0], posargs[1]
                l = []
                for x in xrange(len(t1)):
                    try:
                        l.append((t1[x], t2[x]))
                    except:
                        l.append((t1[x], None))

                l.reverse()
                t = tuple(l)
                nestedhandler(f, t, *pargs, **kwargs)
            return

        return newfunc

    return wrapper


def myhandler(e):
    print 'Caught exception!', e


from salamoia.tests import *
runDocTests()