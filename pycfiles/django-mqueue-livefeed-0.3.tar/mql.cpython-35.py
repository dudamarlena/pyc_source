# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ggg/www/dev/mogos/mogo90/mogo/mqueue_livefeed/templatetags/mql.py
# Compiled at: 2018-01-21 03:08:13
# Size of source mod 2**32: 405 bytes
from django import template
from mqueue.utils import format_event_class, get_admin_url
from mqueue_livefeed.conf import CHANNEL
register = template.Library()

@register.filter
def get_badge(event):
    return format_event_class(event)


@register.simple_tag
def event_admin_url(event):
    return get_admin_url(event)


@register.simple_tag
def mqchannel():
    return CHANNEL