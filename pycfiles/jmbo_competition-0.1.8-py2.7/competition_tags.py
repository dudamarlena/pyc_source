# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hedley/django/instances/foundry/src/jmbo-competition/competition/templatetags/competition_tags.py
# Compiled at: 2013-02-08 02:38:29
from django import template
from django.core.urlresolvers import reverse
register = template.Library()

@register.inclusion_tag('competition/inclusion_tags/competition_detail.html', takes_context=True)
def competition_detail(context, obj):
    can_enter, reason = obj.can_enter(context['request'])
    print can_enter
    print reason
    context.update({'object': obj, 
       'can_enter': can_enter, 
       'reason': reason})
    return context