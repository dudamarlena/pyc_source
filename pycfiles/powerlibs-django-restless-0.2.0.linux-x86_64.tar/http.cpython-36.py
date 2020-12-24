# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cleber/.pyenv/versions/3.6.2/lib/python3.6/site-packages/powerlibs/django/restless/http.py
# Compiled at: 2017-04-19 16:07:32
# Size of source mod 2**32: 2705 bytes
from django import http
from django.core.serializers.json import DjangoJSONEncoder
try:
    import json
except ImportError:
    from django.utils import simplejson as json

__all__ = ['JSONResponse', 'JSONErrorResponse', 'HttpError',
 'Http200', 'Http201', 'Http400', 'Http401', 'Http403']

class JSONResponse(http.HttpResponse):
    __doc__ = 'HTTP response with JSON body ("application/json" content type)'

    def __init__(self, data, **kwargs):
        kwargs['content_type'] = 'application/json; charset=utf-8'
        (super(JSONResponse, self).__init__)(
         json.dumps(data, cls=DjangoJSONEncoder), **kwargs)


class JSONErrorResponse(JSONResponse):
    __doc__ = 'HTTP Error response with JSON body ("application/json" content type)'

    def __init__(self, reason, **additional_data):
        resp = {'error': reason}
        resp.update(additional_data)
        super(JSONErrorResponse, self).__init__(resp)


class Http200(JSONResponse):
    __doc__ = 'HTTP 200 OK'


class Http201(JSONResponse):
    __doc__ = 'HTTP 201 CREATED'
    status_code = 201


class Http400(JSONErrorResponse, http.HttpResponseBadRequest):
    __doc__ = 'HTTP 400 Bad Request'


class Http401(http.HttpResponse):
    __doc__ = 'HTTP 401 UNAUTHENTICATED'
    status_code = 401

    def __init__(self, typ='basic', realm='api'):
        super(Http401, self).__init__()
        if typ == 'basic':
            self['WWW-Authenticate'] = 'Basic realm="%s"' % realm
        else:
            assert False, 'Invalid type ' + str(typ)
            self.status_code = 403


class Http403(JSONErrorResponse, http.HttpResponseForbidden):
    __doc__ = 'HTTP 403 FORBIDDEN'


class Http404(JSONErrorResponse):
    __doc__ = 'HTTP 404 Not Found'
    status_code = 404


class Http409(JSONErrorResponse):
    __doc__ = 'HTTP 409 Conflict'
    status_code = 409


class Http500(JSONErrorResponse):
    __doc__ = 'HTTP 500 Internal Server Error'
    status_code = 500


class HttpError(Exception):
    __doc__ = 'Exception that results in returning a JSONErrorResponse to the user.'

    def __init__(self, code, reason, **additional_data):
        super(HttpError, self).__init__(self, reason)
        self.response = JSONErrorResponse(reason, **additional_data)
        self.response.status_code = code