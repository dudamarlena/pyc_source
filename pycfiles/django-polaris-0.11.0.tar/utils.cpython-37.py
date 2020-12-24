# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jakeurban/Documents/workspace/stellar/django-polaris/polaris/polaris/locale/utils.py
# Compiled at: 2020-04-23 18:52:30
# Size of source mod 2**32: 876 bytes
from typing import Optional
from django.utils import translation
import django.utils.translation as _
from rest_framework.response import Response
from polaris.utils import render_error_response

def validate_language(lang: str, content_type: str='application/json') -> Optional[Response]:
    if not lang:
        return render_error_response((_('Missing language code in request')),
          content_type=content_type)
    else:
        return _is_supported_language(lang) or render_error_response((_('Unsupported language: %s' % lang)),
          content_type=content_type)


def activate_lang_for_request(lang: str):
    translation.activate(lang)


def _is_supported_language(lang: str) -> bool:
    from django.conf.global_settings import LANGUAGES
    return any((lang == supported_lang[0] for supported_lang in LANGUAGES))