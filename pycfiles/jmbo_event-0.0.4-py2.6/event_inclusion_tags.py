# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/event/templatetags/event_inclusion_tags.py
# Compiled at: 2011-10-05 09:29:08
from django import template
register = template.Library()

@register.inclusion_tag('event/inclusion_tags/event_entryitem_listing.html')
def event_entryitem_listing(object_list):
    return {'object_list': object_list}


@register.inclusion_tag('event/inclusion_tags/event_detail.html')
def event_detail(obj):
    return {'object': obj}