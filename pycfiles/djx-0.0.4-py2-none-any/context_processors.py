# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-n_sfyb/Django/django/template/context_processors.py
# Compiled at: 2019-02-14 00:35:17
"""
A set of request processors that return dictionaries to be merged into a
template context. Each function takes the request object as its only parameter
and returns a dictionary to add to the context.

These are referenced from the 'context_processors' option of the configuration
of a DjangoTemplates backend and used by RequestContext.
"""
from __future__ import unicode_literals
import itertools
from django.conf import settings
from django.middleware.csrf import get_token
from django.utils.encoding import force_text
from django.utils.functional import SimpleLazyObject, lazy

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
            return force_text(token)
            return

    return {b'csrf_token': SimpleLazyObject(_get_val)}


def debug(request):
    """
    Returns context variables helpful for debugging.
    """
    context_extras = {}
    if settings.DEBUG and request.META.get(b'REMOTE_ADDR') in settings.INTERNAL_IPS:
        context_extras[b'debug'] = True
        from django.db import connections
        context_extras[b'sql_queries'] = lazy(lambda : list(itertools.chain(*[ connections[x].queries for x in connections ])), list)
    return context_extras


def i18n(request):
    from django.utils import translation
    return {b'LANGUAGES': settings.LANGUAGES, 
       b'LANGUAGE_CODE': translation.get_language(), 
       b'LANGUAGE_BIDI': translation.get_language_bidi()}


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