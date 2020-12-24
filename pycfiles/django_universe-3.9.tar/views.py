# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ubuntu/mydjango/mysite/django_universe/views.py
# Compiled at: 2016-09-09 12:28:46
from django.shortcuts import render, HttpResponse
from django.conf import settings
import json, os

def index(request):
    views_dict = {}
    apps = settings.APPS_FOR_UNIVERSE
    for app in apps:
        list1 = []
        list2 = []
        views_file = os.path.join(settings.BASE_DIR, app, 'views.py')
        for line in file(views_file):
            if line.startswith('def'):
                list1.append(line[4:line.index('(')])

        views_dict[app] = list1

    return HttpResponse(json.dumps(views_dict))