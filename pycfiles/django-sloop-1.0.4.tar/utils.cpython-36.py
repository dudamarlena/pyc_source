# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /app/django_sloop/utils.py
# Compiled at: 2019-08-14 11:46:19
# Size of source mod 2**32: 177 bytes
from django.apps import apps
from .settings import DJANGO_SLOOP_SETTINGS

def get_device_model():
    return (apps.get_model)(*DJANGO_SLOOP_SETTINGS['DEVICE_MODEL'].split('.'))