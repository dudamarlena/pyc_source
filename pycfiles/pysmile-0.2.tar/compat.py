# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pysmi/compat.py
# Compiled at: 2018-12-29 12:21:47
import sys
if sys.version_info[0] > 2:

    def encode(s):
        if isinstance(s, str):
            s = s.encode('utf-8', 'ignore')
        return s


    def decode(s):
        if isinstance(s, bytes):
            s = s.decode('utf-8', 'ignore')
        return s


else:

    def encode(s):
        if isinstance(s, unicode):
            s = s.encode('utf-8', 'ignore')
        return s


    def decode(s):
        if isinstance(s, str):
            s = s.decode('utf-8', 'ignore')
        return s