# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/jmbo/tests/templatetags/tests_template_tags.py
# Compiled at: 2017-05-03 05:57:29
from django import template
register = template.Library()

@register.simple_tag(takes_context=True)
def inject_foo(context):
    context['foo'] = 'bar'
    return ''