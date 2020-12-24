# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/matheus/Documents/projects/enki/Admin-Django/msk/multiuploader/templatetags/multiuploader.py
# Compiled at: 2013-04-04 15:38:21
from django import template
from django.conf import settings
register = template.Library()

@register.inclusion_tag('multiuploader/multiuploader_main.html')
def multiupform():
    return {'static_url': settings.STATIC_URL}