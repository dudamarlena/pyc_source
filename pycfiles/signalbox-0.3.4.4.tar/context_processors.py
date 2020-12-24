# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ben/dev/signalbox/signalbox/context_processors.py
# Compiled at: 2014-08-27 19:26:12
from django.conf import settings

def globals(request):
    return {'BRAND_NAME': settings.BRAND_NAME, 
       'GOOGLE_TRACKING_ID': settings.GOOGLE_TRACKING_ID}