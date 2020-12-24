# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/richcomments/templatetags/richcomments.py
# Compiled at: 2011-09-15 07:47:06
from django import template
from django.template.loader import render_to_string
register = template.Library()

@register.simple_tag
def richcomments_static():
    return render_to_string('richcomments/templatetags/richcomments_static.html')