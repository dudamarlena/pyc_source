# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-intel/egg/meringue/context_processors.py
# Compiled at: 2015-08-17 17:37:49
from django.conf import settings

def base(request):
    return {'SITE_NAME': settings.SITE_NAME, 
       'TEMPLATE_DEBUG': settings.TEMPLATE_DEBUG, 
       'DEBUG': settings.DEBUG}