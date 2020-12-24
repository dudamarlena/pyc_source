# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/dev/dev/django-rest-framework-features/rest_framework_features/urls.py
# Compiled at: 2019-10-07 03:33:53
# Size of source mod 2**32: 457 bytes
from django.urls import NoReverseMatch
from . import schema

def reverse(feature_name, **kwargs):
    feature_schema = schema.get_schema()
    try:
        feature = feature_schema[feature_name]
    except KeyError:
        raise NoReverseMatch(feature_name)
    else:
        return substitute(feature['coerced_url'], kwargs)


def substitute(coerced_url, kwargs):
    return (coerced_url.format)(**kwargs)


__all__ = ('reverse', 'substitute')