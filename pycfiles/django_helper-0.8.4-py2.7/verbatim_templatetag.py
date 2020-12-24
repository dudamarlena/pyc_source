# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/djangohelper/templatetags/verbatim_templatetag.py
# Compiled at: 2012-06-27 03:40:15
"""
from:https://gist.github.com/2409775
jQuery templates use constructs like:

{{if condition}} print something{{/if}}

Or like:

{% if condition %} print {%=object.something %}{% endif %}

This, of course, completely screws up Django templates,
because Django thinks {{ and }} mean something.

Wrap {% verbatim %} and {% endverbatim %} around those
blocks of jQuery templates and this will try its best
to output the contents with no changes.
"""
from django import template
register = template.Library()

class VerbatimNode(template.Node):

    def __init__(self, text):
        self.text = text

    def render(self, context):
        return self.text


@register.tag
def verbatim(parser, token):
    text = []
    while 1:
        token = parser.tokens.pop(0)
        if token.contents == 'endverbatim':
            break
        if token.token_type == template.TOKEN_VAR:
            text.append('{{ ')
        elif token.token_type == template.TOKEN_BLOCK:
            text.append('{%')
        text.append(token.contents)
        if token.token_type == template.TOKEN_VAR:
            text.append(' }}')
        elif token.token_type == template.TOKEN_BLOCK:
            if not text[(-1)].startswith('='):
                text[(-1):(-1)] = [
                 ' ']
            text.append(' %}')

    return VerbatimNode(('').join(text))