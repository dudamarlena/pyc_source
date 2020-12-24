# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/dev/dev/django-rest-framework-features/rest_framework_features/test.py
# Compiled at: 2019-10-07 03:33:53
# Size of source mod 2**32: 683 bytes
from django.urls import NoReverseMatch
from rest_framework.test import APIClient
from . import schema, urls

class FeatureAPIClient(APIClient):

    def __call__(self, feature_name, kwargs=None, **extra):
        feature_schema = schema.get_schema()
        try:
            feature_def = feature_schema[feature_name]
        except KeyError:
            raise NoReverseMatch(feature_name)
        else:
            path = urls.substitute(feature_def['coerced_url'], kwargs or {})
            method = feature_def['http_method_name']
            return (getattr(self, method))(path=path, **extra)


__all__ = ('FeatureAPIClient', )