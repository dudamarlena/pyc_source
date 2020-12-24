# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/competition/templatetags/competition_inclusion_tags.py
# Compiled at: 2010-08-04 03:48:25
from django import template
register = template.Library()

@register.inclusion_tag('competition/inclusion_tags/competition_listing.html')
def competition_listing(object_list):
    return {'object_list': object_list}


@register.inclusion_tag('competition/inclusion_tags/competition_detail.html')
def competition_detail(obj):
    return {'object': obj}