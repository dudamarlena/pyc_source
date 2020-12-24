# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Python27\Lib\site-packages\pysideuic\port_v2\string_io.py
# Compiled at: 2014-04-24 00:47:04
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO