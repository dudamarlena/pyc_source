# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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
    """JSONResponse"""

    def __init__(self, data, **kwargs):
        kwargs['content_type'] = 'application/json; charset=utf-8'
        (super(JSONResponse, self).__init__)(
         json.dumps(data, cls=DjangoJSONEncoder), **kwargs)


class JSONErrorResponse(JSONResponse):
    """JSONErrorResponse"""

    def __init__(self, reason, **additional_data):
        resp = {'error': reason}
        resp.update(additional_data)
        super(JSONErrorResponse, self).__init__(resp)


class Http200(JSONResponse):
    """Http200"""
    pass


class Http201(JSONResponse):
    """Http201"""
    status_code = 201


class Http400(JSONErrorResponse, http.HttpResponseBadRequest):
    """Http400"""
    pass


class Http401(http.HttpResponse):
    """Http401"""
    status_code = 401

    def __init__(self, typ='basic', realm='api'):
        super(Http401, self).__init__()
        if typ == 'basic':
            self['WWW-Authenticate'] = 'Basic realm="%s"' % realm
        else:
            assert False, 'Invalid type ' + str(typ)
            self.status_code = 403


class Http403(JSONErrorResponse, http.HttpResponseForbidden):
    """Http403"""
    pass


class Http404(JSONErrorResponse):
    """Http404"""
    status_code = 404


class Http409(JSONErrorResponse):
    """Http409"""
    status_code = 409


class Http500(JSONErrorResponse):
    """Http500"""
    status_code = 500


class HttpError(Exception):
    """HttpError"""

    def __init__(self, code, reason, **additional_data):
        super(HttpError, self).__init__(self, reason)
        self.response = JSONErrorResponse(reason, **additional_data)
        self.response.status_code = code