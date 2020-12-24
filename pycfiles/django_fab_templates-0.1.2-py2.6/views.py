# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/src/django_fab_templates/templates/vagrant_project/+project+/views.py
# Compiled at: 2011-05-20 17:10:28
from django.http import HttpResponse
from annoying.decorators import render_to

@render_to('home.html')
def home(request):
    return {}