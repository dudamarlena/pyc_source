# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/django/django/views/decorators/csrf.py
# Compiled at: 2018-07-11 18:15:30
import warnings
from django.middleware.csrf import CsrfViewMiddleware, get_token
from django.utils.decorators import decorator_from_middleware, available_attrs
from functools import wraps
csrf_protect = decorator_from_middleware(CsrfViewMiddleware)
csrf_protect.__name__ = 'csrf_protect'
csrf_protect.__doc__ = '\nThis decorator adds CSRF protection in exactly the same way as\nCsrfViewMiddleware, but it can be used on a per view basis.  Using both, or\nusing the decorator multiple times, is harmless and efficient.\n'

class _EnsureCsrfToken(CsrfViewMiddleware):

    def _reject(self, request, reason):
        return


requires_csrf_token = decorator_from_middleware(_EnsureCsrfToken)
requires_csrf_token.__name__ = 'requires_csrf_token'
requires_csrf_token.__doc__ = '\nUse this decorator on views that need a correct csrf_token available to\nRequestContext, but without the CSRF protection that csrf_protect\nenforces.\n'

class _EnsureCsrfCookie(CsrfViewMiddleware):

    def _reject(self, request, reason):
        return

    def process_view(self, request, callback, callback_args, callback_kwargs):
        retval = super(_EnsureCsrfCookie, self).process_view(request, callback, callback_args, callback_kwargs)
        get_token(request)
        return retval


ensure_csrf_cookie = decorator_from_middleware(_EnsureCsrfCookie)
ensure_csrf_cookie.__name__ = 'ensure_csrf_cookie'
ensure_csrf_cookie.__doc__ = '\nUse this decorator to ensure that a view sets a CSRF cookie, whether or not it\nuses the csrf_token template tag, or the CsrfViewMiddleware is used.\n'

def csrf_response_exempt(view_func):
    """
    Modifies a view function so that its response is exempt
    from the post-processing of the CSRF middleware.
    """
    warnings.warn('csrf_response_exempt is deprecated. It no longer performs a function, and calls to it can be removed.', DeprecationWarning)
    return view_func


def csrf_view_exempt(view_func):
    """
    Marks a view function as being exempt from CSRF view protection.
    """
    warnings.warn('csrf_view_exempt is deprecated. Use csrf_exempt instead.', DeprecationWarning)
    return csrf_exempt(view_func)


def csrf_exempt(view_func):
    """
    Marks a view function as being exempt from the CSRF view protection.
    """

    def wrapped_view(*args, **kwargs):
        return view_func(*args, **kwargs)

    wrapped_view.csrf_exempt = True
    return wraps(view_func, assigned=available_attrs(view_func))(wrapped_view)