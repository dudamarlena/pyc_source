# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/herbert/dev/python/sctdev/simpleproject/simpleproject/../../communitytools/sphenecoll/sphene/community/sphpermalink.py
# Compiled at: 2012-03-17 12:42:14


def sphpermalink(func):

    def inner(*args, **kwargs):
        from sphene.community.sphutils import sph_reverse
        bits = func(*args, **kwargs)
        (viewname, args, kwargs) = bits
        return sph_reverse(viewname, args=args, kwargs=kwargs)

    return inner


def get_urlconf():
    from sphene.community.middleware import get_current_request
    return getattr(get_current_request(), 'urlconf', None)