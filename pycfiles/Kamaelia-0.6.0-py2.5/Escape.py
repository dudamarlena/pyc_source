# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/Kamaelia/Support/Data/Escape.py
# Compiled at: 2008-10-19 12:19:52
import re as _re

def escape(message, substring=None):
    result = _re.sub('%', '%25', message)
    if substring is not None:
        for x in substring:
            escaped_x = '%' + hex(ord(x))[2:]
            if x in '.^$*+?{}\\[]|()':
                x = '\\' + x
            result = _re.sub(x, escaped_x, result)

    return result


def unescape(message, substring=None):
    result = message
    if substring is not None:
        for x in substring:
            escaped_x = '%' + hex(ord(x))[2:]
            if x == '\\':
                x = '\\\\'
            result = _re.sub(escaped_x, x, result)

    result = _re.sub('%25', '%', result)
    return result