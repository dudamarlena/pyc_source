# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/django/django/contrib/webdesign/templatetags/webdesign.py
# Compiled at: 2018-07-11 18:15:30
from __future__ import unicode_literals
from django.contrib.webdesign.lorem_ipsum import words, paragraphs
from django import template
register = template.Library()

class LoremNode(template.Node):

    def __init__(self, count, method, common):
        self.count, self.method, self.common = count, method, common

    def render(self, context):
        try:
            count = int(self.count.resolve(context))
        except (ValueError, TypeError):
            count = 1

        if self.method == b'w':
            return words(count, common=self.common)
        paras = paragraphs(count, common=self.common)
        if self.method == b'p':
            paras = [ b'<p>%s</p>' % p for p in paras ]
        return (b'\n\n').join(paras)


@register.tag
def lorem(parser, token):
    """
    Creates random Latin text useful for providing test data in templates.

    Usage format::

        {% lorem [count] [method] [random] %}

    ``count`` is a number (or variable) containing the number of paragraphs or
    words to generate (default is 1).

    ``method`` is either ``w`` for words, ``p`` for HTML paragraphs, ``b`` for
    plain-text paragraph blocks (default is ``b``).

    ``random`` is the word ``random``, which if given, does not use the common
    paragraph (starting "Lorem ipsum dolor sit amet, consectetuer...").

    Examples:
        * ``{% lorem %}`` will output the common "lorem ipsum" paragraph
        * ``{% lorem 3 p %}`` will output the common "lorem ipsum" paragraph
          and two random paragraphs each wrapped in HTML ``<p>`` tags
        * ``{% lorem 2 w random %}`` will output two random latin words
    """
    bits = list(token.split_contents())
    tagname = bits[0]
    common = bits[(-1)] != b'random'
    if not common:
        bits.pop()
    if bits[(-1)] in ('w', 'p', 'b'):
        method = bits.pop()
    else:
        method = b'b'
    if len(bits) > 1:
        count = bits.pop()
    else:
        count = b'1'
    count = parser.compile_filter(count)
    if len(bits) != 1:
        raise template.TemplateSyntaxError(b'Incorrect format for %r tag' % tagname)
    return LoremNode(count, method, common)