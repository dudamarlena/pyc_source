# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/rerb/.virtualenvs/django-credits-demo/lib/python3.5/site-packages/django_credits-0.1.2-py3.5.egg/django_credits/templatetags/django_credits.py
# Compiled at: 2016-07-16 06:05:33
# Size of source mod 2**32: 488 bytes
from django import template
from django.conf import settings
from ..models import Credit
register = template.Library()
DEFAULT_DJANGO_CREDITS_DELAY = 3000

@register.inclusion_tag('django_credits.html')
def django_credits():
    return {'credits': Credit.objects.all(), 
     'django_credits_delay': getattr(settings, 'DJANGO_CREDITS_DELAY', DEFAULT_DJANGO_CREDITS_DELAY)}