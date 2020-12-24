# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cleber/.pyenv/versions/3.6.2/lib/python3.6/site-packages/powerlibs/django/restless/views.py
# Compiled at: 2017-04-19 16:07:32
# Size of source mod 2**32: 4578 bytes
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.http import HttpResponse
from .http import Http200, Http500, HttpError
import traceback, json
__all__ = [
 'Endpoint']

class Endpoint(View):
    __doc__ = '\n    Class-based Django view that should be extended to provide an API\n    endpoint (resource). To provide GET, POST, PUT, HEAD or DELETE methods,\n    implement the corresponding get(), post(), put(), head() or delete()\n    method, respectively.\n\n    If you also implement authenticate(request) method, it will be called\n    before the main method to provide authentication, if needed. Auth mixins\n    use this to provide authentication.\n\n    The usual Django "request" object passed to methods is extended with a\n    few more attributes:\n\n      * request.content_type - the content type of the request\n      * request.params - a dictionary with GET parameters\n      * request.data - a dictionary with POST/PUT parameters, as parsed from\n          either form submission or submitted application/json data payload\n      * request.raw_data - string containing raw request body\n\n    The view method should return either a HTTPResponse (for example, a\n    redirect), or something else (usually a dictionary or a list). If something\n    other than HTTPResponse is returned, it is first serialized into\n    :py:class:`restless.http.JSONResponse` with a status code 200 (OK),\n    then returned.\n\n    The authenticate method should return either a HttpResponse, which will\n    shortcut the rest of the request handling (the view method will not be\n    called), or None (the request will be processed normally).\n\n    Both methods can raise a :py:class:`restless.http.HttpError` exception\n    instead of returning a HttpResponse, to shortcut the request handling and\n    immediately return the error to the client.\n    '

    @staticmethod
    def _parse_content_type(content_type):
        if ';' in content_type:
            ct, params = content_type.split(';', 1)
            try:
                params = dict(param.split('=') for param in params.split())
            except:
                params = {}

        else:
            ct = content_type
            params = {}
        return (
         ct, params)

    def _parse_body(self, request):
        if request.method not in ('POST', 'PUT', 'PATCH'):
            return
        else:
            ct, ct_params = self._parse_content_type(request.content_type)
            if ct == 'application/json':
                charset = ct_params.get('charset', 'utf-8')
                try:
                    data = request.body.decode(charset)
                    request.data = json.loads(data)
                except Exception as ex:
                    raise HttpError(400, 'invalid JSON payload: %s' % ex)

            else:
                if ct == 'application/x-www-form-urlencoded' or ct.startswith('multipart/form-data'):
                    request.data = dict((k, v) for k, v in request.POST.items())
                else:
                    request.data = request.body

    def _process_authenticate(self, request):
        if hasattr(self, 'authenticate'):
            if callable(self.authenticate):
                auth_response = self.authenticate(request)
                if isinstance(auth_response, HttpResponse):
                    return auth_response
                if auth_response is None:
                    pass
                else:
                    raise TypeError('authenticate method must return HttpResponse instance or None')

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        if not hasattr(request, 'content_type'):
            request.content_type = request.META.get('CONTENT_TYPE', 'text/plain')
        request.params = dict((k, v) for k, v in request.GET.items())
        request.data = None
        request.raw_data = request.body
        try:
            self._parse_body(request)
            authentication_required = self._process_authenticate(request)
            if authentication_required:
                return authentication_required
            response = (super(Endpoint, self).dispatch)(request, *args, **kwargs)
        except HttpError as err:
            response = err.response
        except Exception as ex:
            if settings.DEBUG:
                response = Http500((str(ex)), traceback=(traceback.format_exc()))
            else:
                raise

        if not isinstance(response, HttpResponse):
            response = Http200(response)
        return response