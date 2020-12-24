# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/urlographer/utils.py
# Compiled at: 2013-07-23 17:23:48
from django.core.urlresolvers import get_mod_func
from django.utils.importlib import import_module
from django.utils.functional import memoize
_view_cache = {}

def force_ascii(s):
    """
    Eliminate all non-ASCII characters, ignoring errors
    """
    if isinstance(s, unicode):
        return s.encode('ascii', 'ignore')
    else:
        return unicode(s, 'ascii', errors='ignore')


def canonicalize_path(path):
    """
    #. Eliminate extra slashes
    #. Eliminate ./
    #. Make ../ behave as expected by eliminating parent dirs from path
       (but without unintentionally exposing files, of course)
    #. Elminate all unicode chars using :func:`force_ascii`
    """
    while '//' in path:
        path = path.replace('//', '/')

    if path.startswith('./'):
        path = path[1:]
    else:
        if path.startswith('../'):
            path = path[2:]
        while '/./' in path:
            path = path.replace('/./', '/')

        while '/../' in path:
            pre, post = path.split('/../', 1)
            if pre.startswith('/') and '/' in pre[1:]:
                pre = ('/').join(pre.split('/')[:-1])
                path = ('/').join([pre, post])
            else:
                path = '/' + post

    return force_ascii(path.lower())


def get_view(lookup_view):
    """
    Uses similar logic to django.urlresolvers.get_callable, but always raises
    on failures and supports class based views.
    """
    lookup_view = lookup_view.encode('ascii')
    mod_name, func_or_class_name = get_mod_func(lookup_view)
    assert func_or_class_name != ''
    view = getattr(import_module(mod_name), func_or_class_name)
    assert callable(view) or hasattr(view, 'as_view')
    return view


get_view = memoize(get_view, _view_cache, 1)

def force_cache_invalidation(request):
    """
    Returns true if a request from contains the Cache-Control: no-cache header
    """
    return 'no-cache' in request.META.get('HTTP_CACHE_CONTROL', '')