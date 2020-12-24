# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/taurus/core/util/console.py
# Compiled at: 2019-08-19 15:09:29
"""This module contains ANSI color codes"""
from builtins import object
__all__ = [
 'make_color_table', 'NoColors', 'TermColors', 'HTMLColors']
__docformat__ = 'restructuredtext'

def make_color_table(in_class, use_name=False, fake=False):
    """Build a set of color attributes in a class.
    Helper function for building the TermColors classes."""
    color_templates = (
     ('Black', '0;30'),
     ('Red', '0;31'),
     ('Green', '0;32'),
     ('Brown', '0;33'),
     ('Blue', '0;34'),
     ('Purple', '0;35'),
     ('Cyan', '0;36'),
     ('LightGray', '0;37'),
     ('DarkGray', '1;30'),
     ('LightRed', '1;31'),
     ('LightGreen', '1;32'),
     ('Yellow', '1;33'),
     ('LightBlue', '1;34'),
     ('LightPurple', '1;35'),
     ('LightCyan', '1;36'),
     ('White', '1;37'))
    if fake:
        for name, value in color_templates:
            setattr(in_class, name, '')

    elif use_name:
        for name, value in color_templates:
            setattr(in_class, name, in_class._base % name)

    else:
        for name, value in color_templates:
            setattr(in_class, name, in_class._base % value)


class NoColors(object):
    NoColor = ''
    Normal = ''
    _base = ''


class TermColors(object):
    """Color escape sequences.

    This class defines the escape sequences for all the standard (ANSI?)
    colors in terminals. Also defines a NoColor escape which is just the null
    string, suitable for defining 'dummy' color schemes in terminals which get
    confused by color escapes.

    This class should be used as a mixin for building color schemes.

    Basicaly this class is just a copy of IPython.ColorANSI.TermColors class"""
    NoColor = ''
    Normal = '\x1b[0m'
    _base = '\x1b[%sm'


class HTMLColors(object):
    NoColor = ''
    Normal = '</font>'
    _base = '<font color=%s>'


make_color_table(NoColors, fake=True)
make_color_table(TermColors)
make_color_table(HTMLColors, True)