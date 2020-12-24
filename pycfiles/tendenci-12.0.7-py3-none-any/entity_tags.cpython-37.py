# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/apps/entities/templatetags/entity_tags.py
# Compiled at: 2020-03-30 17:48:04
# Size of source mod 2**32: 872 bytes
from django.template import Library
register = Library()

@register.inclusion_tag('entities/options.html', takes_context=True)
def entity_options(context, user, entity):
    context.update({'opt_object':entity, 
     'user':user})
    return context


@register.inclusion_tag('entities/nav.html', takes_context=True)
def entity_nav(context, user, entity=None):
    context.update({'nav_object':entity, 
     'user':user})
    return context


@register.inclusion_tag('entities/search-form.html', takes_context=True)
def entity_search(context):
    return context


@register.inclusion_tag('entities/top_nav_items.html', takes_context=True)
def entity_current_app(context, user, entity=None):
    context.update({'app_object':entity, 
     'user':user})
    print(context.get('nav_object', None))
    return context