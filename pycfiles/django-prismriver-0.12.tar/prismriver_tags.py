# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/PolCPP/Documents/Proyectos/Activos/Django Prismriver/prismriver/templatetags/prismriver_tags.py
# Compiled at: 2012-08-29 20:11:05
from django import template
from django.core.urlresolvers import reverse
from django.template.context import Context
from prismriver.settings import CUSTOM_MENU
from prismriver.views import load_apps, load_custom_models
from prismriver.settings import SIDEBAR_APP_MENU, SIDEBAR_LAST_ACTIONS
from django.template.loader import get_template
from copy import deepcopy
register = template.Library()

def get_custom_menu(request):
    apps = deepcopy(SIDEBAR_APP_MENU)
    for app in apps:
        app['models'], app['enabled'] = load_custom_models(request, app['items'])

    c = Context({'apps': apps, 'custom': True})
    t = get_template('admin/side_menu.html')
    return t.render(c)


def get_menu(request):
    current_url = request.path.replace(reverse('admin:index'), '').lower()
    c = Context({'apps': load_apps(request), 'custom': False})
    t = get_template('admin/side_menu.html')
    return t.render(c)


@register.filter(name='get_apps')
def get_apps(request):
    if CUSTOM_MENU:
        return get_custom_menu(request)
    else:
        return get_menu(request)


@register.tag(name='side_last_actions')
def side_last_actions(request):
    return SIDEBAR_LAST_ACTIONS