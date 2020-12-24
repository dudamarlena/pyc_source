# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-intel/egg/django_rlog/connect.py
# Compiled at: 2016-08-23 01:20:06
from django.conf import settings

def get_connection():
    for key in ['REDIS_CONN', 'REDIS_CLIENT', 'REDIS_CACHE']:
        if hasattr(settings, key):
            return getattr(settings, key)