# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/miltonln/Proyectos/django-menu-generator/menu_generator/templatetags/menu_generator.py
# Compiled at: 2018-01-31 09:35:59
# Size of source mod 2**32: 1207 bytes
from django import template
from django.conf import settings
from .utils import get_menu_from_apps
from .. import defaults
from ..menu import generate_menu
register = template.Library()

@register.simple_tag(takes_context=True)
def get_menu(context, menu_name):
    """
    Returns a consumable menu list for a given menu_name found in settings.py.
    Else it returns an empty list.

    Update, March 18 2017: Now the function get the menu list from settings and append more items if found on the
    menus.py's 'MENUS' dict.
    :param context: Template context
    :param menu_name: String, name of the menu to be found
    :return: Generated menu
    """
    menu_list = getattr(settings, menu_name, defaults.MENU_NOT_FOUND)
    menu_from_apps = get_menu_from_apps(menu_name)
    if menu_list == defaults.MENU_NOT_FOUND:
        if menu_from_apps:
            menu_list = menu_from_apps
    if menu_list != defaults.MENU_NOT_FOUND:
        if menu_from_apps:
            menu_list += menu_from_apps
    return generate_menu(context['request'], menu_list)