# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/django/django/utils/decorators.py
# Compiled at: 2018-07-11 18:15:30
"""Functions that help with dynamically creating decorators for views."""
from functools import wraps, update_wrapper, WRAPPER_ASSIGNMENTS

class classonlymethod(classmethod):

    def __get__(self, instance, owner):
        if instance is not None:
            raise AttributeError('This method is available only on the view class.')
        return super(classonlymethod, self).__get__(instance, owner)


def method_decorator(decorator):
    """
    Converts a function decorator into a method decorator
    """

    def _dec(func):

        def _wrapper(self, *args, **kwargs):

            @decorator
            def bound_func(*args2, **kwargs2):
                return func(self, *args2, **kwargs2)

            return bound_func(*args, **kwargs)

        @decorator
        def dummy(*args, **kwargs):
            pass

        update_wrapper(_wrapper, dummy)
        update_wrapper(_wrapper, func)
        return _wrapper

    update_wrapper(_dec, decorator)
    _dec.__name__ = 'method_decorator(%s)' % decorator.__name__
    return _dec


def decorator_from_middleware_with_args(middleware_class):
    """
    Like decorator_from_middleware, but returns a function
    that accepts the arguments to be passed to the middleware_class.
    Use like::

         cache_page = decorator_from_middleware_with_args(CacheMiddleware)
         # ...

         @cache_page(3600)
         def my_view(request):
             # ...
    """
    return make_middleware_decorator(middleware_class)


def decorator_from_middleware(middleware_class):
    """
    Given a middleware class (not an instance), returns a view decorator. This
    lets you use middleware functionality on a per-view basis. The middleware
    is created with no params passed.
    """
    return make_middleware_decorator(middleware_class)()


def available_attrs(fn):
    """
    Return the list of functools-wrappable attributes on a callable.
    This is required as a workaround for http://bugs.python.org/issue3445.
    """
    return tuple(a for a in WRAPPER_ASSIGNMENTS if hasattr(fn, a))


def make_middleware_decorator(middleware_class):

    def _make_decorator(*m_args, **m_kwargs):
        middleware = middleware_class(*m_args, **m_kwargs)

        def _decorator(view_func):

            @wraps(view_func, assigned=available_attrs(view_func))
            def _wrapped_view(request, *args, **kwargs):
                if hasattr(middleware, 'process_request'):
                    result = middleware.process_request(request)
                    if result is not None:
                        return result
                if hasattr(middleware, 'process_view'):
                    result = middleware.process_view(request, view_func, args, kwargs)
                    if result is not None:
                        return result
                try:
                    response = view_func(request, *args, **kwargs)
                except Exception as e:
                    if hasattr(middleware, 'process_exception'):
                        result = middleware.process_exception(request, e)
                        if result is not None:
                            return result
                    raise

                if hasattr(response, 'render') and callable(response.render):
                    if hasattr(middleware, 'process_template_response'):
                        response = middleware.process_template_response(request, response)
                    if hasattr(middleware, 'process_response'):
                        callback = lambda response: middleware.process_response(request, response)
                        response.add_post_render_callback(callback)
                elif hasattr(middleware, 'process_response'):
                    return middleware.process_response(request, response)
                return response

            return _wrapped_view

        return _decorator

    return _make_decorator