# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/nodeshot/ui/open311_demo/views.py
# Compiled at: 2014-09-02 11:52:33
from django.shortcuts import render
from nodeshot.ui.default.settings import TILESERVER_URL

def open311(request):
    context = {'TILESERVER_URL': TILESERVER_URL}
    return render(request, 'open311/index.html', context)