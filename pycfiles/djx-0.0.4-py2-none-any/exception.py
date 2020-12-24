# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-n_sfyb/Django/django/core/handlers/exception.py
# Compiled at: 2019-02-14 00:35:17
from __future__ import unicode_literals
import logging, sys, warnings
from functools import wraps
from django.conf import settings
from django.core import signals
from django.core.exceptions import PermissionDenied, RequestDataTooBig, SuspiciousOperation, TooManyFieldsSent
from django.http import Http404
from django.http.multipartparser import MultiPartParserError
from django.urls import get_resolver, get_urlconf
from django.utils.decorators import available_attrs
from django.utils.deprecation import RemovedInDjango20Warning
from django.utils.encoding import force_text
from django.views import debug
logger = logging.getLogger(b'django.request')

def convert_exception_to_response(get_response):
    """
    Wrap the given get_response callable in exception-to-response conversion.

    All exceptions will be converted. All known 4xx exceptions (Http404,
    PermissionDenied, MultiPartParserError, SuspiciousOperation) will be
    converted to the appropriate response, and all other exceptions will be
    converted to 500 responses.

    This decorator is automatically applied to all middleware to ensure that
    no middleware leaks an exception and that the next middleware in the stack
    can rely on getting a response instead of an exception.
    """

    @wraps(get_response, assigned=available_attrs(get_response))
    def inner(request):
        try:
            response = get_response(request)
        except Exception as exc:
            response = response_for_exception(request, exc)

        return response

    return inner


def response_for_exception(request, exc):
    if isinstance(exc, Http404):
        if settings.DEBUG:
            response = debug.technical_404_response(request, exc)
        else:
            response = get_exception_response(request, get_resolver(get_urlconf()), 404, exc)
    elif isinstance(exc, PermissionDenied):
        logger.warning(b'Forbidden (Permission denied): %s', request.path, extra={b'status_code': 403, b'request': request})
        response = get_exception_response(request, get_resolver(get_urlconf()), 403, exc)
    elif isinstance(exc, MultiPartParserError):
        logger.warning(b'Bad request (Unable to parse request body): %s', request.path, extra={b'status_code': 400, b'request': request})
        response = get_exception_response(request, get_resolver(get_urlconf()), 400, exc)
    elif isinstance(exc, SuspiciousOperation):
        if isinstance(exc, (RequestDataTooBig, TooManyFieldsSent)):
            request._mark_post_parse_error()
        security_logger = logging.getLogger(b'django.security.%s' % exc.__class__.__name__)
        security_logger.error(force_text(exc), extra={b'status_code': 400, b'request': request})
        if settings.DEBUG:
            response = debug.technical_500_response(request, status_code=400, *sys.exc_info())
        else:
            response = get_exception_response(request, get_resolver(get_urlconf()), 400, exc)
    elif isinstance(exc, SystemExit):
        raise
    else:
        signals.got_request_exception.send(sender=None, request=request)
        response = handle_uncaught_exception(request, get_resolver(get_urlconf()), sys.exc_info())
    if not getattr(response, b'is_rendered', True) and callable(getattr(response, b'render', None)):
        response = response.render()
    return response


def get_exception_response(request, resolver, status_code, exception, sender=None):
    try:
        callback, param_dict = resolver.resolve_error_handler(status_code)
        try:
            response = callback(request, **dict(param_dict, exception=exception))
        except TypeError:
            warnings.warn(b'Error handlers should accept an exception parameter. Update your code as this parameter will be required in Django 2.0', RemovedInDjango20Warning, stacklevel=2)
            response = callback(request, **param_dict)

    except Exception:
        signals.got_request_exception.send(sender=sender, request=request)
        response = handle_uncaught_exception(request, resolver, sys.exc_info())

    return response


def handle_uncaught_exception(request, resolver, exc_info):
    """
    Processing for any otherwise uncaught exceptions (those that will
    generate HTTP 500 responses).
    """
    if settings.DEBUG_PROPAGATE_EXCEPTIONS:
        raise
    logger.error(b'Internal Server Error: %s', request.path, exc_info=exc_info, extra={b'status_code': 500, b'request': request})
    if settings.DEBUG:
        return debug.technical_500_response(request, *exc_info)
    callback, param_dict = resolver.resolve_error_handler(500)
    return callback(request, **param_dict)