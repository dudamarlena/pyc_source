# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: //bigfoot/grimmhelga/Production/scripts/libraries/nuke\pysideuic\port_v2\as_string.py
# Compiled at: 2014-04-23 23:47:04
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