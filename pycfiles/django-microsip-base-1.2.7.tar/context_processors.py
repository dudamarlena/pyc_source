# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\repositorios\web\django-microsip-base\django_microsip_base\django_microsip_base\context_processors.py
# Compiled at: 2020-04-28 20:23:37
from django.conf import settings
import importlib

def menu(request):
    context = {'menu': []}
    selected_app = 'Inicio'
    items = []
    if '/administrador/' in request.path:
        selected_app = 'Administrador'
    else:
        for app in settings.EXTRA_APPS:
            if app['url_main_path'] in request.path:
                selected_app = app['name']

        context_menu = {'name': selected_app, 'selected_app': selected_app, 
           'icon_class': 'glyphicon glyphicon-home', 
           'items': items}
        for app in settings.EXTRA_APPS:
            if request.user.username in app['users'] or not app['users']:
                context_menu['items'].append({'name': app['name'], 'url': app['url'], 'icon_class': app['icon_class']})

    context['menu'] = context_menu
    return context