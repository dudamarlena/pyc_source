# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hedley/django/instances/django-link/link/templatetags/link_tags.py
# Compiled at: 2017-07-06 07:47:29
# Size of source mod 2**32: 340 bytes
from django import template
from link.models import Link
register = template.Library()

@register.inclusion_tag('link/inclusion_tags/link_detail.html', takes_context=True)
def render_link(context, slug):
    try:
        context['object'] = Link.objects.get(slug=slug)
    except Link.DoesNotExist:
        pass

    return context