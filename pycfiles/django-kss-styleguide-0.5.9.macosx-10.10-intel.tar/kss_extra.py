# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/tim/Projects/django_kss/VENV/lib/python2.7/site-packages/django_kss/templatetags/kss_extra.py
# Compiled at: 2014-12-20 07:08:46
from django import template
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter
from pygments.util import ClassNotFound
register = template.Library()

@register.filter(name='highlight_code')
def highlight_code(code, lang):
    if code is not None:
        try:
            lexer = get_lexer_by_name(lang, encoding='utf-8', stripall=True, startinline=True)
        except ClassNotFound:
            lexer = get_lexer_by_name('text')

        formatter = HtmlFormatter(encoding='utf-8', style='colorful', cssclass='highlight', lineanchors='line')
        return highlight(code, lexer, formatter)
    else:
        return code
        return