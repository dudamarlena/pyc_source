# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/travis/virtualenv/python2.7.15/lib/python2.7/site-packages/coolamqp/framing/compilation/utilities.py
# Compiled at: 2020-04-03 16:00:47
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