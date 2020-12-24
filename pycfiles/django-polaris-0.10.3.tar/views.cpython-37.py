# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jakeurban/Documents/workspace/stellar/django-polaris/polaris/polaris/locale/views.py
# Compiled at: 2020-02-04 17:51:52
# Size of source mod 2**32: 1541 bytes
from typing import Optional
from django.utils import translation
import django.utils.translation as _
from rest_framework.renderers import JSONRenderer
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import api_view, renderer_classes
from polaris.helpers import render_error_response, check_authentication

def validate_language(lang: str, content_type: str='application/json') -> Optional[Response]:
    if not lang:
        return render_error_response((_('Missing language code in request')),
          content_type=content_type)
    else:
        return _is_supported_language(lang) or render_error_response((_('Unsupported language: %s' % lang)),
          content_type=content_type)


def activate_lang_for_request(lang: str):
    translation.activate(lang)


@api_view(['GET', 'POST'])
@renderer_classes([JSONRenderer])
@check_authentication()
def language(request: Request) -> Response:
    if request.method == 'GET':
        return Response({'language': translation.get_language()})
    lang = request.POST.get('language')
    err_resp = validate_language(lang)
    if err_resp:
        return err_resp
    translation.activate(lang)
    request.session[translation.LANGUAGE_SESSION_KEY] = lang
    return Response({'language': lang})


def _is_supported_language(lang: str) -> bool:
    from django.conf.global_settings import LANGUAGES
    return any((lang == supported_lang[0] for supported_lang in LANGUAGES))