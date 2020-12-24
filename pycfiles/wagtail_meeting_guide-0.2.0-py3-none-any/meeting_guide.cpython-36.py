# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/tallen/projects/wagtail-meeting-guide/meeting_guide/templatetags/meeting_guide.py
# Compiled at: 2019-12-27 18:00:06
# Size of source mod 2**32: 300 bytes
from django import template
register = template.Library()

@register.inclusion_tag('meeting_guide/tags/meeting_guide.html', takes_context=True)
def meeting_guide(context):
    """
    Display the ReactJS drive Meeting Guide list.
    """
    return {'mapbox_key': context['mapbox_key']}