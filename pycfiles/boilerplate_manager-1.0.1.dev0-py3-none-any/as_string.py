# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: C:\symlinks\repos\boilerplate_dcc_pyside_widget\boilerplate_dcc_pyside_widget\lib\third_party\pysideuic\port_v2\as_string.py
# Compiled at: 2015-08-04 11:44:30
import re

def as_string(obj, encode=True):
    if isinstance(obj, basestring):
        s = '"' + _escape(obj.encode('UTF-8')) + '"'
        return s
    return str(obj)


_esc_regex = re.compile('(\\"|\\\'|\\\\)')

def _escape(text):
    x = _esc_regex.sub('\\\\\\1', text)
    return re.sub('\\n', '\\\\n"\\n"', x)