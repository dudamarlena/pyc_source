# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/apps/event_logs/templatetags/event_log_tags.py
# Compiled at: 2020-02-26 14:48:40
# Size of source mod 2**32: 943 bytes
from django.template import Library
register = Library()

@register.inclusion_tag('event_logs/options.html', takes_context=True)
def event_log_options(context, user, event_log):
    context.update({'opt_object':event_log, 
     'user':user})
    return context


@register.inclusion_tag('event_logs/nav.html', takes_context=True)
def event_log_nav(context, user, event_log=None):
    context.update({'nav_object':event_log, 
     'user':user})
    return context


@register.inclusion_tag('event_logs/top_nav_items.html', takes_context=True)
def event_log_current_app(context, user, event_log=None):
    context.update({'app_object':event_log, 
     'user':user})
    return context


@register.inclusion_tag('event_logs/search-form.html', takes_context=True)
def event_log_search(context, search_form):
    context.update({'search_form': search_form})
    return context