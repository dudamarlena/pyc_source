# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/django-tastypie-legacy/tastypie/http.py
# Compiled at: 2018-07-11 18:15:32
"""
The various HTTP responses for use in returning proper HTTP codes.
"""
from __future__ import unicode_literals
from django.http import HttpResponse

class HttpCreated(HttpResponse):
    status_code = 201

    def __init__(self, *args, **kwargs):
        location = kwargs.pop(b'location', b'')
        super(HttpCreated, self).__init__(*args, **kwargs)
        self[b'Location'] = location


class HttpAccepted(HttpResponse):
    status_code = 202


class HttpNoContent(HttpResponse):
    status_code = 204

    def __init__(self, *args, **kwargs):
        super(HttpNoContent, self).__init__(*args, **kwargs)
        del self[b'Content-Type']


class HttpMultipleChoices(HttpResponse):
    status_code = 300


class HttpSeeOther(HttpResponse):
    status_code = 303


class HttpNotModified(HttpResponse):
    status_code = 304


class HttpBadRequest(HttpResponse):
    status_code = 400


class HttpUnauthorized(HttpResponse):
    status_code = 401


class HttpForbidden(HttpResponse):
    status_code = 403


class HttpNotFound(HttpResponse):
    status_code = 404


class HttpMethodNotAllowed(HttpResponse):
    status_code = 405


class HttpConflict(HttpResponse):
    status_code = 409


class HttpGone(HttpResponse):
    status_code = 410


class HttpUnprocessableEntity(HttpResponse):
    status_code = 422


class HttpTooManyRequests(HttpResponse):
    status_code = 429


class HttpApplicationError(HttpResponse):
    status_code = 500


class HttpNotImplemented(HttpResponse):
    status_code = 501