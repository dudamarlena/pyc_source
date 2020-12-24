# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/greenlight/_greenlight.py
# Compiled at: 2010-10-17 14:49:21
from functools import wraps
from gevent.greenlet import Greenlet
from gevent.event import AsyncResult
from .utils import hide_stderr
__all__ = ['greenlight', 'greenlight_nostart', 'green_return']

class _Greenlight_Return(Exception):
    """
    Special exception, so we can break out of the generator.
    """

    def __init__(self, value):
        self.value = value


def green_return(value):
    """
    Raise our special exception, signaling the generator to stop and return the
value.
    """
    raise _Greenlight_Return(value)


def _greenlight(result, generator, asyncresult):
    if getattr(generator, 'send', None) is None:
        asyncresult.set(generator)
        return asyncresult
    else:
        waiting = [
         True, None]
        while True:
            isgreenlet = isinstance(result, Greenlet)
            try:
                if isgreenlet:
                    try:
                        value = result.get(False)
                    except Exception, e:
                        generator.throw(result.exception)

                else:
                    value = result
                result = generator.send(value)
            except StopIteration:
                asyncresult.set(result.value if isgreenlet else result)
                return asyncresult
            except _Greenlight_Return, e:
                asyncresult.set(e.value)
                return asyncresult
            except Exception, e:
                asyncresult.set_exception(e)
                return asyncresult
            else:
                if isinstance(result, Greenlet):
                    hide_stderr(result)

                    def onresult(res):
                        if waiting[0]:
                            waiting[0] = False
                            waiting[1] = res
                        else:
                            _greenlight(res, generator, asyncresult)

                    result.link(onresult)
                    if waiting[0]:
                        waiting[0] = False
                        return asyncresult
                    result = waiting[1]
                    waiting[0] = True
                    waiting[1] = None

        return asyncresult


def greenlight_nostart(f):

    @wraps(f)
    def inner(*args, **kwargs):

        @wraps(f)
        def more_inner():
            res = AsyncResult()
            _greenlight(None, f(*args, **kwargs), res)
            return res.get()

        g = Greenlet(more_inner)
        hide_stderr(g)
        return g

    return inner


def greenlight(f):

    @wraps(f)
    def inner(*args, **kwargs):
        g = greenlight_nostart(f)(*args, **kwargs)
        g.start()
        return g

    return inner