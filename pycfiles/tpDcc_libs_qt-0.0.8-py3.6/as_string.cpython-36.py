# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tpDcc/libs/qt/externals/pysideuic/port_v2/as_string.py
# Compiled at: 2020-04-15 12:12:43
# Size of source mod 2**32: 1307 bytes
import re

def as_string(obj, encode=True):
    if isinstance(obj, basestring):
        s = '"' + _escape(obj.encode('UTF-8')) + '"'
        return s
    else:
        return str(obj)


_esc_regex = re.compile('(\\"|\\\'|\\\\)')

def _escape(text):
    x = _esc_regex.sub('\\\\\\1', text)
    return re.sub('\\n', '\\\\n"\\n"', x)