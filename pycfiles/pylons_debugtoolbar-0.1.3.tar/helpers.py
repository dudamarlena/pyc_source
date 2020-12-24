# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/pylonsgenshi/helpers.py
# Compiled at: 2008-01-03 15:48:25
from webhelpers import *
try:
    from minwebhelpers import *
    _HAVE_MINWEBHELPERS = True
except ImportError:
    _HAVE_MINWEBHELPERS = False

from genshi.builder import tag
from genshi.core import Markup as _Markup

def _wrap_helpers(localdict):

    def helper_wrapper(func):

        def wrapped_helper(*args, **kw):
            return _Markup(func(*args, **kw))

        wrapped_helper.__name__ = func.__name__
        return wrapped_helper

    for (name, func) in localdict.iteritems():
        if not callable(func) or not func.__module__.startswith('webhelpers.rails'):
            continue
        localdict[name] = helper_wrapper(func)

    if _HAVE_MINWEBHELPERS:
        localdict['javascript_include_tag'] = helper_wrapper(javascript_include_tag)
        localdict['stylesheet_link_tag'] = helper_wrapper(stylesheet_link_tag)


_wrap_helpers(locals())
__all__ = [ __name for __name in locals().keys() if not __name.startswith('_') ]