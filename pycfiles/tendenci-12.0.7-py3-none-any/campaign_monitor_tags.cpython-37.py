# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/apps/campaign_monitor/templatetags/campaign_monitor_tags.py
# Compiled at: 2020-02-26 14:48:40
# Size of source mod 2**32: 1223 bytes
from django.template import Library
from django.conf import settings
register = Library()

@register.inclusion_tag('campaign_monitor/templates/options.html', takes_context=True)
def template_options(context, user, template):
    context.update({'opt_object':template, 
     'user':user, 
     'cm_url':settings.CAMPAIGNMONITOR_URL})
    return context


@register.inclusion_tag('campaign_monitor/templates/nav.html', takes_context=True)
def template_nav(context, user, template=None):
    context.update({'nav_object':template, 
     'user':user, 
     'cm_url':settings.CAMPAIGNMONITOR_URL})
    return context


@register.inclusion_tag('campaign_monitor/campaigns/options.html', takes_context=True)
def campaign_options(context, user, campaign):
    context.update({'opt_object':campaign, 
     'user':user, 
     'cm_url':settings.CAMPAIGNMONITOR_URL})
    return context


@register.inclusion_tag('campaign_monitor/campaigns/nav.html', takes_context=True)
def campaign_nav(context, user, campaign=None):
    context.update({'nav_object':campaign, 
     'user':user, 
     'cm_url':settings.CAMPAIGNMONITOR_URL})
    return context