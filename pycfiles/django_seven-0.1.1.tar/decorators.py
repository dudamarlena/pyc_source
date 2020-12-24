# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/iwoca/django-seven/django_seven/compat/decorators.py
# Compiled at: 2016-07-26 15:41:40
from functools import wraps
from django.conf import settings

def to_tuple(version):
    return tuple(map(lambda x: int(x), version.split('.')))


def available_on(min_supported_version, max_supported_version):

    def wrapped_parameters(func):

        @wraps(func)
        def inner(*args, **kwargs):
            if to_tuple(settings.SEVEN_CURRENT_DJANGO_VERSION) > to_tuple(min_supported_version) and to_tuple(settings.SEVEN_FUTURE_DJANGO_VERSION) < to_tuple(max_supported_version):
                return func(*args, **kwargs)
            raise Exception(('You cannot use {function_name} in your context').format(function_name=str(func)))

        return inner

    return wrapped_parameters