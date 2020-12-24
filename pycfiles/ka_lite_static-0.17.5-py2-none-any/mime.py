# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/django-tastypie-legacy/tastypie/utils/mime.py
# Compiled at: 2018-07-11 18:15:32
from __future__ import unicode_literals
import mimeparse
from tastypie.exceptions import BadRequest

def determine_format(request, serializer, default_format=b'application/json'):
    """
    Tries to "smartly" determine which output format is desired.

    First attempts to find a ``format`` override from the request and supplies
    that if found.

    If no request format was demanded, it falls back to ``mimeparse`` and the
    ``Accepts`` header, allowing specification that way.

    If still no format is found, returns the ``default_format`` (which defaults
    to ``application/json`` if not provided).

    NOTE: callers *must* be prepared to handle BadRequest exceptions due to
          malformed HTTP request headers!
    """
    format = request.GET.get(b'format')
    if format:
        if format in serializer.formats:
            return serializer.get_mime_for_format(format)
    if b'callback' in request.GET:
        return serializer.get_mime_for_format(b'jsonp')
    accept = request.META.get(b'HTTP_ACCEPT', b'*/*')
    if accept != b'*/*':
        try:
            best_format = mimeparse.best_match(serializer.supported_formats_reversed, accept)
        except ValueError:
            raise BadRequest(b'Invalid Accept header')

        if best_format:
            return best_format
    return default_format


def build_content_type(format, encoding=b'utf-8'):
    """
    Appends character encoding to the provided format if not already present.
    """
    if b'charset' in format:
        return format
    if format in ('application/json', 'text/javascript'):
        return format
    return b'%s; charset=%s' % (format, encoding)