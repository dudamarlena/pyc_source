# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hedley/django/instances/django-ultracache/ultracache/decorators.py
# Compiled at: 2019-05-31 04:23:36
import hashlib, types
from functools import wraps
from django.conf import settings
from django.core.cache import cache
from django.http import HttpResponse
from django.template.response import TemplateResponse
from django.utils.decorators import available_attrs
from django.views.generic.base import TemplateResponseMixin
from ultracache import _thread_locals
from ultracache.utils import cache_meta, get_current_site_pk

def cached_get(timeout, *params):
    """Decorator applied specifically to a view's get method"""

    def decorator(view_func):

        @wraps(view_func, assigned=available_attrs(view_func))
        def _wrapped_view(view_or_request, *args, **kwargs):
            request = getattr(view_or_request, 'request', view_or_request)
            if request.method.lower() not in ('get', 'head'):
                return view_func(view_or_request, *args, **kwargs)
            else:
                l = 0
                try:
                    l = len(request._messages)
                except (AttributeError, TypeError):
                    pass

                if l:
                    return view_func(view_or_request, *args, **kwargs)
                li = [
                 str(view_or_request.__class__), view_func.__name__]
                if not set(params).intersection(set(('request.get_full_path()', 'request.path',
                                                     'request.path_info'))):
                    li.append(request.get_full_path())
                if 'django.contrib.sites' in settings.INSTALLED_APPS:
                    li.append(get_current_site_pk(request))
                keys = list(kwargs.keys())
                keys.sort()
                for key in keys:
                    li.append('%s,%s' % (key, kwargs[key]))

                for param in params:
                    if not isinstance(param, str):
                        param = str(param)
                    li.append(eval(param))

                s = (':').join([ str(l) for l in li ])
                hashed = hashlib.md5(s.encode('utf-8')).hexdigest()
                cache_key = 'ucache-get-%s' % hashed
                cached = cache.get(cache_key, None)
                if cached is None:
                    _thread_locals.ultracache_recorder = []
                    response = view_func(view_or_request, *args, **kwargs)
                    content = None
                    if isinstance(response, TemplateResponse):
                        content = response.render().rendered_content
                    elif isinstance(response, HttpResponse):
                        content = response.content
                    if content is not None:
                        headers = getattr(response, '_headers', {})
                        cache.set(cache_key, {'content': content, 'headers': headers}, timeout)
                        cache_meta(_thread_locals.ultracache_recorder, cache_key, request=request)
                else:
                    response = HttpResponse(cached['content'])
                    for k, v in cached['headers'].items():
                        response[v[0]] = v[1]

                return response

        return _wrapped_view

    return decorator


def ultracache(timeout, *params):
    """Decorator applied to a view class. The get method is decorated
    implicitly."""

    def decorator(cls):

        class WrappedClass(cls):

            def __init__(self, *args, **kwargs):
                super(WrappedClass, self).__init__(*args, **kwargs)

            @cached_get(timeout, *params)
            def get(self, *args, **kwargs):
                return super(WrappedClass, self).get(*args, **kwargs)

        return WrappedClass

    return decorator