# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/django_s3_storage2/conf.py
# Compiled at: 2015-11-24 02:14:29
# Size of source mod 2**32: 2613 bytes
from __future__ import unicode_literals
from django.conf import settings

class LazySetting(object):
    __doc__ = '\n    A proxy to a named Django setting.\n    '

    def __init__(self, name, default=''):
        self.name = name
        self.default = default

    def __get__(self, obj, cls):
        if obj is None:
            return self
        return getattr(obj._settings, self.name, self.default)


class LazySettings(object):
    __doc__ = '\n    A proxy to s3-specific django settings.\n\n    Settings are resolved at runtime, allowing tests\n    to change settings at runtime.\n    '

    def __init__(self, settings):
        self._settings = settings

    AWS_REGION = LazySetting(name='AWS_REGION', default='us-east-1')
    AWS_ACCESS_KEY_ID = LazySetting(name='AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = LazySetting(name='AWS_SECRET_ACCESS_KEY')
    AWS_S3_BUCKET_NAME = LazySetting(name='AWS_S3_BUCKET_NAME')
    AWS_S3_CALLING_FORMAT = LazySetting(name='AWS_S3_CALLING_FORMAT', default='boto.s3.connection.OrdinaryCallingFormat')
    AWS_S3_KEY_PREFIX = LazySetting(name='AWS_S3_KEY_PREFIX')
    AWS_S3_BUCKET_AUTH = LazySetting(name='AWS_S3_BUCKET_AUTH', default=True)
    AWS_S3_MAX_AGE_SECONDS = LazySetting(name='AWS_S3_MAX_AGE_SECONDS', default=3600)
    AWS_S3_PUBLIC_URL = LazySetting(name='AWS_S3_PUBLIC_URL')
    AWS_S3_REDUCED_REDUNDANCY = LazySetting(name='AWS_S3_REDUCED_REDUNDANCY')
    AWS_S3_BUCKET_NAME_STATIC = LazySetting(name='AWS_S3_BUCKET_NAME_STATIC')
    AWS_S3_CALLING_FORMAT_STATIC = LazySetting(name='AWS_S3_CALLING_FORMAT_STATIC', default='boto.s3.connection.OrdinaryCallingFormat')
    AWS_S3_KEY_PREFIX_STATIC = LazySetting(name='AWS_S3_KEY_PREFIX_STATIC')
    AWS_S3_BUCKET_AUTH_STATIC = LazySetting(name='AWS_S3_BUCKET_AUTH_STATIC', default=False)
    AWS_S3_MAX_AGE_SECONDS_STATIC = LazySetting(name='AWS_S3_MAX_AGE_SECONDS_STATIC', default=31536000)
    AWS_S3_PUBLIC_URL_STATIC = LazySetting(name='AWS_S3_PUBLIC_URL_STATIC')
    AWS_S3_REDUCED_REDUNDANCY_STATIC = LazySetting(name='AWS_S3_REDUCED_REDUNDANCY_STATIC')


settings = LazySettings(settings)