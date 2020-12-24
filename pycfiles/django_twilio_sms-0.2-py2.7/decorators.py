# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\django_twilio_sms\decorators.py
# Compiled at: 2013-08-27 16:08:15
from __future__ import unicode_literals
from functools import wraps
import logging
from django.conf import settings
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseNotAllowed
from django.utils import six
from django.utils.encoding import force_text
from django.views.decorators.csrf import csrf_exempt
from twilio.twiml import Verb
from twilio.util import RequestValidator
logger = logging.getLogger(b'django-twilio-sms.decorators')

def twilio_view(f):
    """This decorator provides several helpful shortcuts for writing Twilio
    views.

        - It ensures that only requests from Twilio are passed through. This
          helps protect you from forged requests.

        - It ensures your view is exempt from CSRF checks via Django's
          @csrf_exempt decorator. This is necessary for any view that accepts
          POST requests from outside the local domain (eg: Twilio's servers).

        - It allows your view to (optionally) return TwiML to pass back to
          Twilio's servers instead of building a ``HttpResponse`` object
          manually.

        - It allows your view to (optionally) return any ``twilio.Verb`` object
          instead of building a ``HttpResponse`` object manually.

    Usage::

        from twilio.twiml import Response

        @twilio_view
        def my_view(request):
            r = Response()
            r.sms("Thanks for the SMS message!")
            return r
    """

    @csrf_exempt
    @wraps(f)
    def decorator(request, *args, **kwargs):
        if request.method != b'POST':
            logger.error(b'Twilio: Expected POST request', extra={b'request': request})
            return HttpResponseNotAllowed(request.method)
        else:
            if not getattr(settings, b'TWILIO_SKIP_SIGNATURE_VALIDATION'):
                try:
                    validator = RequestValidator(settings.TWILIO_AUTH_TOKEN)
                    url = request.build_absolute_uri()
                    if b'HTTP_X_FORWARDED_SERVER' in request.META:
                        protocol = b'https' if request.META[b'HTTP_X_TWILIO_SSL'] == b'Enabled' else b'http'
                        url = (b'{0}://{1}{2}').format(protocol, request.META[b'HTTP_X_FORWARDED_SERVER'], request.META[b'REQUEST_URI'])
                    signature = request.META[b'HTTP_X_TWILIO_SIGNATURE']
                except (AttributeError, KeyError) as e:
                    logger.exception(b'Twilio: Missing META param', extra={b'request': request})
                    return HttpResponseForbidden(b'Missing META param: %s' % e)

                if not validator.validate(url, request.POST, signature):
                    logger.error(b'Twilio: Invalid url signature %s - %s - %s', url, request.POST, signature, extra={b'request': request})
                    return HttpResponseForbidden(b'Invalid signature')
            response = f(request, *args, **kwargs)
            if isinstance(response, six.text_type):
                return HttpResponse(response, mimetype=b'application/xml')
            if isinstance(response, Verb):
                return HttpResponse(force_text(response), mimetype=b'application/xml')
            return response

    return decorator