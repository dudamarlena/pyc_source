# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/django/django/core/context_processors.py
# Compiled at: 2018-07-11 18:15:30
"""
A set of request processors that return dictionaries to be merged into a
template context. Each function takes the request object as its only parameter
and returns a dictionary to add to the context.

These are referenced from the setting TEMPLATE_CONTEXT_PROCESSORS and used by
RequestContext.
"""
from __future__ import unicode_literals
from django.conf import settings
from django.middleware.csrf import get_token
from django.utils import six
from django.utils.encoding import smart_text
from django.utils.functional import lazy

def csrf(request):
    """
    Context processor that provides a CSRF token, or the string 'NOTPROVIDED' if
    it has not been provided by either a view decorator or the middleware
    """

    def _get_val():
        token = get_token(request)
        if token is None:
            return b'NOTPROVIDED'
        else:
            return smart_text(token)
            return

    _get_val = lazy(_get_val, six.text_type)
    return {b'csrf_token': _get_val()}


def debug(request):
    """Returns context variables helpful for debugging."""
    context_extras = {}
    if settings.DEBUG and request.META.get(b'REMOTE_ADDR') in settings.INTERNAL_IPS:
        context_extras[b'debug'] = True
        from django.db import connection
        context_extras[b'sql_queries'] = connection.queries
    return context_extras


def i18n(request):
    from django.utils import translation
    context_extras = {}
    context_extras[b'LANGUAGES'] = settings.LANGUAGES
    context_extras[b'LANGUAGE_CODE'] = translation.get_language()
    context_extras[b'LANGUAGE_BIDI'] = translation.get_language_bidi()
    return context_extras


def tz(request):
    from django.utils import timezone
    return {b'TIME_ZONE': timezone.get_current_timezone_name()}


def static(request):
    """
    Adds static-related context variables to the context.

    """
    return {b'STATIC_URL': settings.STATIC_URL}


def media(request):
    """
    Adds media-related context variables to the context.

    """
    return {b'MEDIA_URL': settings.MEDIA_URL}


def request(request):
    return {b'request': request}