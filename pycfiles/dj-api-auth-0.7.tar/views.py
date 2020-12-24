# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/fanfei/Documents/Code/dj-api-auth/example/djapp/djapp/views.py
# Compiled at: 2015-06-06 18:55:27
from django.http import HttpResponse

def index(request):
    return HttpResponse('hello, index')