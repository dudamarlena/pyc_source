# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/dusty/code/egetime/venv/lib/python2.7/site-packages/djason/templatetags/tmpl.py
# Compiled at: 2010-11-28 12:59:35
from django.template import Library, TextNode, TOKEN_BLOCK, TOKEN_VAR
register = Library()

@register.tag
def jqtmpl(parser, token):
    nodes = []
    t = parser.next_token()
    while not (t.token_type == TOKEN_BLOCK and t.contents == 'endjqtmpl'):
        if t.token_type == TOKEN_BLOCK:
            nodes.extend(['{%', t.contents, '%}'])
        elif t.token_type == TOKEN_VAR:
            nodes.extend(['{{', t.contents, '}}'])
        else:
            nodes.append(t.contents)
        t = parser.next_token()

    return TextNode(('').join(nodes))