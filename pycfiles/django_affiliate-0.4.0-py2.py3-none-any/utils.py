# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/stalk/develop/django_affiliate/django-affiliate/affiliate/utils.py
# Compiled at: 2015-10-28 03:20:13
from django.utils.http import urlencode
from django.utils.six.moves.urllib.parse import parse_qsl, urlparse, urlunparse
from . import app_settings
try:
    from django.apps import apps
    get_model = apps.get_model
except ImportError:
    from django.db.models.loading import get_model as django_get_model

    def get_model(app_label, model_name=None):
        if model_name is None:
            app_label, model_name = app_label.split('.')
        return django_get_model(app_label, model_name)


def get_affiliate_model():
    return get_model(app_settings.AFFILIATE_MODEL)


def add_affiliate_code(url, aid_code):
    parsed = urlparse(str(url))
    query = dict(parse_qsl(parsed.query))
    query.update({app_settings.PARAM_NAME: str(aid_code)})
    url_parts = list(parsed)
    url_parts[4] = urlencode(query)
    return urlunparse(url_parts)


def remove_affiliate_code(url):
    parsed = urlparse(str(url))
    query = dict(parse_qsl(parsed.query))
    query.pop(app_settings.PARAM_NAME, None)
    url_parts = list(parsed)
    url_parts[4] = urlencode(query)
    return urlunparse(url_parts)