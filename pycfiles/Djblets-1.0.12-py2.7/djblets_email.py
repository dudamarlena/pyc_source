# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/djblets/util/templatetags/djblets_email.py
# Compiled at: 2019-06-12 01:17:17
from __future__ import unicode_literals
import re
from django import template
from django.utils.safestring import mark_safe
from djblets.util.compat.django.template.loader import render_to_string
from djblets.util.decorators import blocktag
register = template.Library()

@register.simple_tag(takes_context=True)
def quoted_email(context, template_name):
    """
    Renders a specified template as a quoted reply, using the current context.
    """
    return quote_text(render_to_string(template_name, context))


@register.tag
@blocktag
def condense(context, nodelist, max_newlines=3):
    """Condenses a block of text.

    This will ensure that there are never more than the given number of
    consecutive newlines. It's particularly useful when formatting plain text
    output, to avoid issues with template tags adding unwanted newlines.
    """
    text = nodelist.render(context).strip()
    text = re.sub(b'\\n{%d,}' % (max_newlines + 1), b'\n' * max_newlines, text)
    return text


@register.filter
def quote_text(text, level=1):
    """
    Quotes a block of text the specified number of times.
    """
    lines = text.split(b'\n')
    quoted = b''
    for line in lines:
        quoted += b'%s%s\n' % (b'> ' * level, line)

    return mark_safe(quoted.rstrip())