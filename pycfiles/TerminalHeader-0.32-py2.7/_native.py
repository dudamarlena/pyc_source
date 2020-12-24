# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\theader\markupsafe\_native.py
# Compiled at: 2016-01-25 01:09:29
"""
    markupsafe._native
    ~~~~~~~~~~~~~~~~~~

    Native Python implementation the C module is not compiled.

    :copyright: (c) 2010 by Armin Ronacher.
    :license: BSD, see LICENSE for more details.
"""
from markupsafe import Markup
from markupsafe._compat import text_type

def escape(s):
    """Convert the characters &, <, >, ' and " in string s to HTML-safe
    sequences.  Use this if you need to display text that might contain
    such characters in HTML.  Marks return value as markup string.
    """
    if hasattr(s, '__html__'):
        return s.__html__()
    return Markup(text_type(s).replace('&', '&amp;').replace('>', '&gt;').replace('<', '&lt;').replace("'", '&#39;').replace('"', '&#34;'))


def escape_silent(s):
    """Like :func:`escape` but converts `None` into an empty
    markup string.
    """
    if s is None:
        return Markup()
    else:
        return escape(s)


def soft_unicode(s):
    """Make a string unicode if it isn't already.  That way a markup
    string is not converted back to unicode.
    """
    if not isinstance(s, text_type):
        s = text_type(s)
    return s