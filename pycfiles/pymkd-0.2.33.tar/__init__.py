# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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