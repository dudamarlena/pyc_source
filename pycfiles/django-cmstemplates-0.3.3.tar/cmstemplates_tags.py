# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/asyncee/git/django-cmstemplates/cmstemplates/templatetags/cmstemplates_tags.py
# Compiled at: 2016-02-24 04:47:52
from __future__ import print_function, unicode_literals
from django import template
from cmstemplates import queries as q
register = template.Library()

@register.simple_tag(takes_context=True)
def cms_group(context, name, description=b''):
    template_group = q.get_template_group(name, description)
    content = q.get_cached_content_for_group(template_group)
    return template.Template(content).render(context)