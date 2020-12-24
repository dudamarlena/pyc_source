# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Volumes/Ozgur/Sites/senpilic.com.tr/senpilic/utils/templatetags/linebreaksli.py
# Compiled at: 2012-10-03 06:31:29
import re
from django import template
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe
register = template.Library()

def needs_autoescape_register(filter):
    filter = register.filter(filter)
    filter.needs_autoescape = True
    return filter


@needs_autoescape_register
def linebreaksli(value, autoescape=None):
    """Break a string down based on newline characters and for each line, enclose it in the <li> and </li> without the <ul> and </ul> tags. 
           Similar to the unordered_list filter but not requiring a list"""
    if autoescape:
        esc = conditional_escape
    else:
        esc = lambda x: x
    if value:
        value = re.sub('\\r\\n|\\r|\\n', '\n', value)
        paras = re.split('\n', value)
    else:
        paras = []
    paras = [ '<li>%s</li>' % esc(p.strip()).replace('\\n', '<br/>') for p in paras ]
    return mark_safe(('\n\n').join(paras))