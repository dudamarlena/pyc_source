# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/apps/dashboard/templatetags/dashboard_tags.py
# Compiled at: 2020-02-26 14:48:40
# Size of source mod 2**32: 1033 bytes
import simplejson
from django.template import Library
from tendenci.apps.dashboard.models import DashboardStat
register = Library()

@register.inclusion_tag('dashboard/nav.html', takes_context=True)
def dashboard_nav(context, user):
    context.update({'user': user})
    return context


@register.inclusion_tag('dashboard/stats.html', takes_context=True)
def dashboard_stat(context, stat_type):
    value = ''
    type_name = ''
    label = ''
    stat = DashboardStat.objects.get_latest(stat_type)
    if stat:
        value = simplejson.loads((stat.value), use_decimal=True)
        type_name = stat_type.name
        label = stat_type.description
    context.update({'type_name':type_name, 
     'label':label, 
     'value':value})
    return context


@register.inclusion_tag('dashboard/top_nav_items.html', takes_context=True)
def dashboard_current_app(context, user, dashboard=None):
    context.update({'app_object':dashboard, 
     'user':user})
    return context