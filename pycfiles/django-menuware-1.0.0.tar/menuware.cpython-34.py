# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/val/Projects/.mpro-virenv/bizdir/lib/python3.4/site-packages/menuware/templatetags/menuware.py
# Compiled at: 2016-08-18 14:52:30
# Size of source mod 2**32: 491 bytes
from django import template
from django.conf import settings
from ..menu import generate_menu
from .. import defaults as defs
register = template.Library()

@register.assignment_tag(takes_context=True)
def get_menu(context, menu_name):
    """
    Returns a consumable menu list for a given menu_name found in settings.py.
    Else it returns an empty list.
    """
    menu_list = getattr(settings, menu_name, defs.MENU_NOT_FOUND)
    return generate_menu(context['request'], menu_list)