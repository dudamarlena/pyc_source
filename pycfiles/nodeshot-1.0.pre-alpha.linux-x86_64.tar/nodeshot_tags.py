# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/nodeshot/ui/default/templatetags/nodeshot_tags.py
# Compiled at: 2014-12-28 17:59:16
from django import template
from leaflet.templatetags.leaflet_tags import leaflet_map
register = template.Library()

@register.inclusion_tag('leaflet/_load_map.html')
def nodeshot_map(name, callback=None, fitextent=True, creatediv=True, loadevent='load'):
    return leaflet_map(name, callback=None, fitextent=True, creatediv=True, loadevent='load')