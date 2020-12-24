# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/swainn/projects/tethysdev/django-tethys_apps/tethys_apps/views.py
# Compiled at: 2014-10-09 19:14:14
from django.shortcuts import render
from tethys_apps.app_harvester import SingletonAppHarvester

def library(request):
    """
    Handle the library view
    """
    harvester = SingletonAppHarvester()
    context = {'apps': harvester.apps}
    return render(request, 'tethys_apps/app_library.html', context)