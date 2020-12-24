# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/bouma/gitprojects/provgroningen/buildout/src/djinn_forms/djinn_forms/templatetags/djinn_forms.py
# Compiled at: 2014-05-08 06:45:05
from djinn_core.utils import urn_to_object
from django.template import Library
register = Library()

@register.inclusion_tag('djinn_forms/snippets/link.html')
def link_as_a(link):
    ctx = {}
    _link = link.split('::')[0]
    if _link.startswith('urn'):
        obj = urn_to_object(_link)
        ctx['url'] = obj.get_absolute_url()
        ctx['title'] = obj.title
    else:
        ctx['url'] = ctx['title'] = _link
    ctx['target'] = link.split('::')[1] or ''
    return ctx