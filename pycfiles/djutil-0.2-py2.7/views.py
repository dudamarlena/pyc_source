# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\djutil\views.py
# Compiled at: 2013-07-14 16:33:08
from __future__ import unicode_literals
from django.conf import settings
from django.http import HttpResponseServerError
from django.template import loader, Context

def server_error(request, template_name=b'500.html'):
    t = loader.get_template(template_name)
    ctx = Context({b'request': request, 
       b'MEDIA_URL': settings.MEDIA_URL, 
       b'STATIC_URL': settings.STATIC_URL})
    return HttpResponseServerError(t.render(ctx))