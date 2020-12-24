# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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