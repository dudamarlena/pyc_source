# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/apps/contacts/templatetags/contact_tags.py
# Compiled at: 2020-02-26 14:48:40
# Size of source mod 2**32: 840 bytes
from django.template import Library
register = Library()

@register.inclusion_tag('contacts/options.html', takes_context=True)
def contact_options(context, user, contact):
    context.update({'opt_object':contact, 
     'user':user})
    return context


@register.inclusion_tag('contacts/nav.html', takes_context=True)
def contact_nav(context, user, contact=None):
    context.update({'nav_object':contact, 
     'user':user})
    return context


@register.inclusion_tag('contacts/search-form.html', takes_context=True)
def contact_search(context):
    return context


@register.inclusion_tag('contacts/top_nav_items.html', takes_context=True)
def contact_current_app(context, user, contact=None):
    context.update({'app_object':contact, 
     'user':user})
    return context