# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/fanfei/Documents/Code/dj-sso-client/example/ssoclient/ssoclient/views.py
# Compiled at: 2015-03-11 19:34:46
from django.shortcuts import render_to_response
from django.template import RequestContext

def home(request):
    context = RequestContext(request)
    return render_to_response('index.html', {'req': request}, context_instance=context)