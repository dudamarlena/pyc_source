# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/wsgi.py
# Compiled at: 2019-08-16 17:27:46
from __future__ import absolute_import
import os, os.path, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), os.pardir))
from django.conf import settings
if not settings.configured:
    from sentry.runner import configure
    configure()
if settings.SESSION_FILE_PATH and not os.path.exists(settings.SESSION_FILE_PATH):
    try:
        os.makedirs(settings.SESSION_FILE_PATH)
    except OSError:
        pass

from django.core.handlers.wsgi import WSGIHandler

class FileWrapperWSGIHandler(WSGIHandler):
    """A WSGIHandler implementation that handles a StreamingHttpResponse
    from django to leverage wsgi.file_wrapper for delivering large streaming
    responses.

    Note: this was added natively into Django 1.8, so if by some reason,
    we upgraded, this wouldn't be relevant anymore."""

    def __call__(self, environ, start_response):
        response = super(FileWrapperWSGIHandler, self).__call__(environ, start_response)
        if hasattr(response, 'streaming') and response.streaming:
            try:
                response = environ['wsgi.file_wrapper'](response.streaming_content)
            except KeyError:
                pass

        return response


application = FileWrapperWSGIHandler()