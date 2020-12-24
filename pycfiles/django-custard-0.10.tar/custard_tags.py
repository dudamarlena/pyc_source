# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/lucio/Projects/django-custard/lib/python2.7/site-packages/custard/templatetags/custard_tags.py
# Compiled at: 2014-07-29 04:15:43
from django import template
import logging
logger = logging.getLogger(__name__)
register = template.Library()

@register.simple_tag
def debug(value):
    """
        Simple tag to debug output a variable;

        Usage:
            {% debug request %}
    """
    print '%s %s: ' % (type(value), value)
    print dir(value)
    print '\n\n'
    return ''