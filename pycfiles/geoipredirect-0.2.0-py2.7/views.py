# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/geoip/views.py
# Compiled at: 2011-01-28 12:21:03
from django.http import HttpResponse

def save_target(request):
    response = HttpResponse()
    if request.POST['save']:
        response.set_cookie('geoip-target', request.POST['target'])
    else:
        unset(request.COOKIES['geoip-target'])
    return response