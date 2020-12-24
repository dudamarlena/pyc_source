# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/gizmo/templatetags/gizmo_test_tags.py
# Compiled at: 2011-10-05 09:22:31
from django import template
register = template.Library()

@register.simple_tag
def test_simple_tag():
    return 'test simple tag result'