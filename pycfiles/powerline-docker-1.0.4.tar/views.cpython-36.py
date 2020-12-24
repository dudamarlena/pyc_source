# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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
    """Endpoint"""

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
        return (ct, params)

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