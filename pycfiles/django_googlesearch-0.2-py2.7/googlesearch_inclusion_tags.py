# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/googlesearch/templatetags/googlesearch_inclusion_tags.py
# Compiled at: 2015-04-21 15:30:36
from django import template
register = template.Library()

@register.inclusion_tag('googlesearch/inclusion_tags/form.html', takes_context=True)
def googlesearch_form(context):
    return context


@register.inclusion_tag('googlesearch/inclusion_tags/results.html')
def googlesearch_results():
    return {}