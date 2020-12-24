# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tpDcc/libs/qt/externals/pysideuic/port_v2/string_io.py
# Compiled at: 2020-05-13 19:31:15
# Size of source mod 2**32: 976 bytes
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO