# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ben/Projects/django-basic-blog/blog/templatetags/markdownify.py
# Compiled at: 2015-12-14 10:55:36
from django import template
from markdown import markdown
register = template.Library()

@register.filter('markdownify')
def markdownify(text):
    return markdown(text)