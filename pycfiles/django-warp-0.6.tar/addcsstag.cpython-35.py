# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/enrico/Dropbox/dev/django-warp/django_warp/templatetags/addcsstag.py
# Compiled at: 2016-01-15 04:40:08
# Size of source mod 2**32: 170 bytes
from django import template
register = template.Library()

@register.filter(name='addcss')
def addcss(field, css):
    return field.as_widget(attrs={'class': css})