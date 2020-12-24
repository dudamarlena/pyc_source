# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/tinycms/templatetags/tinycms_tags.py
# Compiled at: 2015-01-08 08:44:19
from django import template
from django.utils import translation
from django.http import Http404
from tinycms.models import *
register = template.Library()

@register.simple_tag(takes_context=True)
def show_contents(context, value_name, contentTag=None):
    """Show cms content.

    Variables:
    value_name -- value_name of contents to be shown.
    contentTag -- When contentTag is not None, Each content is tagged by contentTag like <contentTag>content</contentTag>
    """
    if value_name not in context:
        raise Http404
    valList = context[value_name]
    result = ''
    for item in valList:
        if contentTag:
            result += '<%s>%s</%s>' % (contentTag, item, contentTag)
        else:
            result += '%s' % item

    return result