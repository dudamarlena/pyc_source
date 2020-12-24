# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sitefilter/templatetags/sitefilter_tags.py
# Compiled at: 2012-11-20 08:29:49
from django import template
from django.contrib.sites.models import Site
from sitefilter.models import get_current_site_filter
register = template.Library()

@register.inclusion_tag('sitefilter/sitefilter.html', takes_context=True)
def sitefilter(context):
    site_filter = get_current_site_filter(context['request'])
    return {'object_list': Site.objects.all(), 
       'selected': site_filter.sites.all()}