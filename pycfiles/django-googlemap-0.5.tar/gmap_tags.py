# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/gmy/project/xperiment/xperiment/googlemap/templatetags/gmap_tags.py
# Compiled at: 2014-04-28 23:20:33
from django import template
from ..utils import get_location_by_ip
register = template.Library()

@register.inclusion_tag('gmap/mark_location.html', takes_context=True)
def mark_location(context, ip_list, width=None, height=400):
    location_list = [ get_location_by_ip(ip) for ip in ip_list ]
    context.update({'location_list': location_list, 
       'width': '%d%s' % (width, 'px') if width else '100%', 
       'height': '%d%s' % (height, 'px'), 
       'is_resize': 'false'})
    return context