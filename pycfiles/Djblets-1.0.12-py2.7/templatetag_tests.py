# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/djblets/extensions/test/templatetag_tests/templatetags/templatetag_tests.py
# Compiled at: 2019-06-12 01:17:17
from __future__ import unicode_literals
from django import template
register = template.Library()

@register.simple_tag
def my_extension_template_tag():
    return b'Hello, world!'