# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pymk/__init__.py
# Compiled at: 2013-12-18 09:40:24
import re
VERSION = '0.4.1'

def compare_version(a, b, separator='.', ignorecase=True):

    def _preprocess(v, separator, ignorecase):
        if ignorecase:
            v = v.lower()
        return [ int(x) if x.isdigit() else [ int(y) if y.isdigit() else y for y in re.findall('\\d+|[a-zA-Z]+', x) ] for x in v.split(separator) ]

    a = _preprocess(a, separator, ignorecase)
    b = _preprocess(b, separator, ignorecase)
    return (a > b) - (a < b)