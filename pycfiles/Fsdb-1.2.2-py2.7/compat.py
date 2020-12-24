# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/fsdb/compat.py
# Compiled at: 2016-03-24 14:09:36
import sys
ISPYTHON2 = sys.version_info[0] < 3
if ISPYTHON2:
    string_types = basestring
else:
    string_types = str