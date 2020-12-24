# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/apps/donations/templatetags/donation_tags.py
# Compiled at: 2020-02-26 14:48:40
# Size of source mod 2**32: 630 bytes
from django.template import Library
register = Library()

@register.inclusion_tag('donations/nav.html', takes_context=True)
def donation_nav(context, user, donation=None):
    context.update({'nav_object':donation, 
     'user':user})
    return context


@register.inclusion_tag('donations/top_nav_items.html', takes_context=True)
def donation_current_app(context, user, donation=None):
    context.update({'app_object':donation, 
     'user':user})
    return context


@register.inclusion_tag('donations/search-form.html', takes_context=True)
def donation_search(context):
    return context