# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/leslie/dev/pkg/django-skeleton/skeleton/views.py
# Compiled at: 2020-04-19 18:42:34
# Size of source mod 2**32: 187 bytes
from django.http import HttpResponse

def site_index(request):
    return HttpResponse('this is the SITE index')


def index(request):
    return HttpResponse('this is the (app) index')