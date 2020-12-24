# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/apps/redirects/templatetags/redirect_tags.py
# Compiled at: 2020-02-26 14:48:40
# Size of source mod 2**32: 854 bytes
from django.template import Library
register = Library()

@register.inclusion_tag('redirects/options.html', takes_context=True)
def redirect_options(context, user, redirect):
    context.update({'opt_object':redirect, 
     'user':user})
    return context


@register.inclusion_tag('redirects/nav.html', takes_context=True)
def redirect_nav(context, user, redirect=None):
    context.update({'nav_object':redirect, 
     'user':user})
    return context


@register.inclusion_tag('redirects/top_nav_items.html', takes_context=True)
def redirect_current_app(context, user, redirect=None):
    context.update({'app_object':redirect, 
     'user':user})
    return context


@register.inclusion_tag('redirects/search-form.html', takes_context=True)
def redirect_search(context):
    return context