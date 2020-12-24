# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/notifications/templatetags/markdown_email.py
# Compiled at: 2020-02-11 04:03:56
from __future__ import unicode_literals
import markdown
from django import template
from django.utils.safestring import mark_safe
from djblets.markdown import markdown_unescape
register = template.Library()

@register.filter
def markdown_email_html(text, is_rich_text):
    if not is_rich_text:
        return text
    return mark_safe(markdown.markdown(text, output_format=b'xhtml1', extensions=[
     b'markdown.extensions.fenced_code',
     b'markdown.extensions.codehilite',
     b'markdown.extensions.tables',
     b'markdown.extensions.sane_lists',
     b'markdown.extensions.smart_strong',
     b'pymdownx.tilde',
     b'djblets.markdown.extensions.escape_html',
     b'djblets.markdown.extensions.wysiwyg_email'], extension_configs={b'codehilite': {b'noclasses': True}}))


@register.filter
def markdown_email_text(text, is_rich_text):
    if not is_rich_text:
        return text
    return markdown_unescape(text)