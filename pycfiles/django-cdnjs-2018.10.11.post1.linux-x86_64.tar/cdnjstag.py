# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/cdnjs/templatetags/cdnjstag.py
# Compiled at: 2018-10-11 08:57:00
from __future__ import unicode_literals
from django import template
from cdnjs import CDNStorage
register = template.Library()
cdn_manager = CDNStorage()

@register.simple_tag(name=b'cdn')
def cdn_static(name, filename=None):
    """
    Returns static file url
    :param name: Is the repository name.
    :param filename:
    :return:
    """
    return cdn_manager.get(name, filename)