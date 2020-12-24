# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/apps/user_groups/templatetags/user_group_tags.py
# Compiled at: 2020-02-26 14:48:40
# Size of source mod 2**32: 840 bytes
from django.template import Library
register = Library()

@register.inclusion_tag('user_groups/options.html', takes_context=True)
def user_group_options(context, user, group):
    context.update({'group':group, 
     'user':user})
    return context


@register.inclusion_tag('user_groups/nav.html', takes_context=True)
def user_group_nav(context, user, group=None):
    context.update({'nav_object':group, 
     'user':user})
    return context


@register.inclusion_tag('user_groups/top_nav_items.html', takes_context=True)
def user_group_current_app(context, user, group=None):
    context.update({'app_object':group, 
     'user':user})
    return context


@register.inclusion_tag('user_groups/search-form.html', takes_context=True)
def group_search(context):
    return context