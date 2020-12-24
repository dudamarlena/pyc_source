# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/urb/Dropbox/dev/django-warp/django_warp/templatetags/addcss_tag.py
# Compiled at: 2016-05-24 07:06:26
# Size of source mod 2**32: 170 bytes
from django import template
register = template.Library()

@register.filter(name='addcss')
def addcss(value, css):
    return value.as_widget(attrs={'class': css})