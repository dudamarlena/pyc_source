# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /var/apps/emerge/playground/django-react/app/myproject/richcontentblocks/templatetags/rich_content_block_tags.py
# Compiled at: 2015-08-18 19:09:38
from django import template
from django.template.loader import render_to_string
from django.template.base import TemplateSyntaxError
from django.utils.encoding import force_text
from myproject.richcontentblocks.models import Content
register = template.Library()

@register.simple_tag
def rich_content_block(key):
    obj = Content.get_content_by_key(key=key)
    if obj:
        return obj.content
    else:
        return 'Content object does not exist.'