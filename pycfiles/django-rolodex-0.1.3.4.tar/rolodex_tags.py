# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jon/DMN/Scripts/django-rolodex/rolodex/templatetags/rolodex_tags.py
# Compiled at: 2015-09-22 01:38:44
from django import template
register = template.Library()
import os, re

@register.filter
def fileBaseName(string):
    return re.sub('(.+)\\?.+', '\\1', os.path.basename(string))