# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/dadasu/demo/django/dj-translate/autotranslate/templatetags/autotranslate.py
# Compiled at: 2016-10-06 05:48:42
from django import template
from django.utils.safestring import mark_safe
from django.utils.html import escape
import re
from django.template import Node
import six
register = template.Library()
rx = re.compile('(%(\\([^\\s\\)]*\\))?[sd]|\\{[\\w\\d_]+?\\})')

def format_message(message):
    return mark_safe(rx.sub('<code>\\1</code>', escape(message).replace('\\n', '<br />\n')))


format_message = register.filter(format_message)

def lines_count(message):
    return 1 + sum([ len(line) / 50 for line in message.split('\n') ])


lines_count = register.filter(lines_count)

def mult(a, b):
    return int(a) * int(b)


mult = register.filter(mult)

def minus(a, b):
    try:
        return int(a) - int(b)
    except:
        return 0


minus = register.filter(minus)

def gt(a, b):
    try:
        return int(a) > int(b)
    except:
        return False


gt = register.filter(gt)

def do_incr(parser, token):
    args = token.split_contents()
    if len(args) < 2:
        raise SyntaxError("'incr' tag requires at least one argument")
    name = args[1]
    if not hasattr(parser, '_namedIncrNodes'):
        parser._namedIncrNodes = {}
    if name not in parser._namedIncrNodes:
        parser._namedIncrNodes[name] = IncrNode(0)
    return parser._namedIncrNodes[name]


do_incr = register.tag('increment', do_incr)

class IncrNode(template.Node):

    def __init__(self, init_val=0):
        self.val = init_val

    def render(self, context):
        self.val += 1
        return six.text_type(self.val)


def is_fuzzy(message):
    return message and hasattr(message, 'flags') and 'fuzzy' in message.flags


is_fuzzy = register.filter(is_fuzzy)

class AutotranslateCsrfTokenPlaceholder(Node):

    def render(self, context):
        return mark_safe('<!-- csrf token placeholder -->')


def autotranslate_csrf_token(parser, token):
    try:
        from django.template.defaulttags import csrf_token
        return csrf_token(parser, token)
    except ImportError:
        return AutotranslateCsrfTokenPlaceholder()


autotranslate_csrf_token = register.tag(autotranslate_csrf_token)