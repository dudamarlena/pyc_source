# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/craterdome/work/django_common/lib/python2.7/site-packages/django_common/decorators.py
# Compiled at: 2012-03-11 19:20:35
try:
    from functools import wraps
except ImportError:
    from django.utils.functional import wraps

import inspect
from django.conf import settings
from django.http import HttpResponseRedirect

def ssl_required(allow_non_ssl=False):
    """Views decorated with this will always get redirected to https except when allow_non_ssl is set to true."""

    def wrapper(view_func):

        def _checkssl(request, *args, **kwargs):
            if hasattr(settings, 'SSL_ENABLED') and settings.SSL_ENABLED and not request.is_secure() and not allow_non_ssl:
                return HttpResponseRedirect(request.build_absolute_uri().replace('http://', 'https://'))
            return view_func(request, *args, **kwargs)

        return _checkssl

    return wrapper


def disable_for_loaddata(signal_handler):
    """
    See: https://code.djangoproject.com/ticket/8399
    Disables signal from firing if its caused because of loaddata
    """

    @wraps(signal_handler)
    def wrapper(*args, **kwargs):
        for fr in inspect.stack():
            if inspect.getmodulename(fr[1]) == 'loaddata':
                return

        signal_handler(*args, **kwargs)

    return wrapper