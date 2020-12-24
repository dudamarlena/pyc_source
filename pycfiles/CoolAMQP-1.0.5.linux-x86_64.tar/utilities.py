# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/virtualenv/python2.7.15/lib/python2.7/site-packages/coolamqp/framing/compilation/utilities.py
# Compiled at: 2020-05-06 12:56:42
from __future__ import absolute_import, division, print_function
import six

def as_unicode(clbl):

    def roll(*args, **kwargs):
        return six.text_type(clbl(*args, **kwargs))

    return roll


@as_unicode
def format_field_name(field):
    if field in ('global', 'type'):
        field = field + '_'
    return field.replace('-', '_')