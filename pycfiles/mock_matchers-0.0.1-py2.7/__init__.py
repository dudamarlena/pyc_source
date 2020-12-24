# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.4-x86_64/egg/mock_matchers/__init__.py
# Compiled at: 2014-09-02 08:51:06


class Matchers(object):

    def __getattribute__(self, item):
        import hamcrest
        if hasattr(hamcrest, item):
            thing = getattr(hamcrest, item)
            if callable(thing):
                return self._wrap(getattr(hamcrest, item))
            return thing
        return object.__getattribute__(self, item)

    def _wrap(self, obj):
        from functools import wraps
        from hamcrest.core.base_matcher import BaseMatcher

        @wraps(obj)
        def __inner(*a, **kwargs):
            resp = obj(*a, **kwargs)
            if isinstance(resp, BaseMatcher):
                meth = lambda s, o: s.matches(o)
                resp.__class__.__eq__ = meth
            return resp

        return __inner


import sys
sys.modules['mock_matchers'] = Matchers()