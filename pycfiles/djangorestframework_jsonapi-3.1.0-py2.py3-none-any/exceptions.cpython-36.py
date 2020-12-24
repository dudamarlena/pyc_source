# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/sao/src/github/django-json-api/django-rest-framework-json-api/rest_framework_json_api/exceptions.py
# Compiled at: 2020-01-23 12:40:39
# Size of source mod 2**32: 1740 bytes
from django.utils.translation import gettext_lazy as _
from rest_framework import exceptions, status
from rest_framework_json_api import utils
from .settings import json_api_settings

def rendered_with_json_api(view):
    from rest_framework_json_api.renderers import JSONRenderer
    for renderer_class in getattr(view, 'renderer_classes', []):
        if issubclass(renderer_class, JSONRenderer):
            return True

    return False


def exception_handler(exc, context):
    from rest_framework.views import exception_handler as drf_exception_handler
    response = drf_exception_handler(exc, context)
    if not response:
        return response
    else:
        is_json_api_view = rendered_with_json_api(context['view'])
        is_uniform = json_api_settings.UNIFORM_EXCEPTIONS
        if not is_json_api_view:
            if not is_uniform:
                return response
        response = utils.format_drf_errors(response, context, exc)
        if not is_json_api_view:
            response.data = utils.format_errors(response.data)
        return response


class Conflict(exceptions.APIException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = _('Conflict.')