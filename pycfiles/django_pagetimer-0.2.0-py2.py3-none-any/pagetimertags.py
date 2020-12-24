# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/anders/work/python/django-pagetimer/pagetimer/templatetags/pagetimertags.py
# Compiled at: 2016-05-09 12:52:27
from django import template
from django.conf import settings
from django.core.urlresolvers import reverse
register = template.Library()

@register.inclusion_tag('pagetimer/pagetimer.html', takes_context=True)
def pagetimer(context):
    interval = 60
    if hasattr(settings, 'PAGETIMER_INTERVAL'):
        interval = settings.PAGETIMER_INTERVAL
    return {'pagetimer_endpoint': reverse('pagetimer-endpoint'), 'pagetimer_interval': interval}