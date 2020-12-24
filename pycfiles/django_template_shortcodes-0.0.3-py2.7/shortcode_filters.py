# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-intel/egg/shortcodes/templatetags/shortcode_filters.py
# Compiled at: 2014-06-19 05:16:18
from shortcodes import parser
from django import template
register = template.Library()

def shortcodes_replace(value, request=None):
    """
    A filter for parsing a string on the format ``[shortcode keyword=value]``
    using the shortcodes parser method.
    """
    return parser.parse(value, request)


register.filter('shortcodes', shortcodes_replace)

def shortcodes_remove(value, request=None):
    """
    A filter for removing shortcodes and the content inside them.
    """
    return parser.remove(value, request)


register.filter('removeshortcodes', shortcodes_remove)