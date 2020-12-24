# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/swainn/projects/tethysdev/django-tethys_apps/tethys_apps/context_processors.py
# Compiled at: 2014-10-09 19:14:14
from tethys_apps.app_harvester import SingletonAppHarvester

def tethys_apps_context(request):
    """
    Add the current Tethys app metadata to the template context.
    """
    harvester = SingletonAppHarvester()
    context = {'tethys_app': None}
    apps_root = 'apps'
    url = request.path
    url_parts = url.split('/')
    if apps_root in url_parts:
        app_root_url_index = url_parts.index(apps_root) + 1
        app_root_url = url_parts[app_root_url_index]
        apps = harvester.apps
        for app in apps:
            if app.root_url == app_root_url:
                context['tethys_app'] = {'name': app.name, 'index': app.index, 'icon': app.icon, 
                   'color': app.color}

    return context