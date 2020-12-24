# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mick/src/django-postal/src/postal/templatetags/postal_tags.py
# Compiled at: 2010-11-18 16:57:45
from django import template
from django.core.urlresolvers import reverse
register = template.Library()

@register.inclusion_tag('postal/monitor_country_change.html')
def monitor_country_change():
    return {'postal_url': reverse('changed_country')}