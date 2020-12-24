# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/tinycms/views.py
# Compiled at: 2014-10-18 23:48:00
from django.http import Http404
from models import *

def show_page(request, url):
    """Return HttpResponse of url
    """
    return Dispatcher.dispatch(url, request)