# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/marcin/projekty/goc-congress/congress/klaus/templatetags/klaus.py
# Compiled at: 2013-11-30 15:24:50
import re
from django import template
register = template.Library()

@register.filter
def shorten_sha1(sha1):
    if re.match('[a-z\\d]{20,40}', sha1):
        sha1 = sha1[:10]
    return sha1