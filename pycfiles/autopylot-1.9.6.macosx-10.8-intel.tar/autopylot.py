# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mattcaldwell/.virtualenvs/autopylot/lib/python2.7/site-packages/autopylot/django/templatetags/autopylot.py
# Compiled at: 2013-11-26 22:17:25
from datetime import datetime
from django import template
register = template.Library()

@register.filter(name='getkey')
def getkey(value, arg):
    """ Gets a value from a dict by key.  This allows keys to contain spaces, dashes, etc. """
    return value.get(arg, '')


@register.filter(name='split')
def split(value, arg):
    return value.split(arg)


@register.filter(name='todatetime')
def todatetime(value, arg=''):
    try:
        dtobj = datetime.strptime(value, '%a, %d %b %Y %H:%M:%S %Z')
    except Exception as e:
        dtobj = ''

    return dtobj