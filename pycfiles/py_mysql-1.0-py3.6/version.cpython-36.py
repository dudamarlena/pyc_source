# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\py_mysql\lib\mysql\connector\version.py
# Compiled at: 2017-12-07 02:34:36
# Size of source mod 2**32: 1583 bytes
"""MySQL Connector/Python version information

The file version.py gets installed and is available after installation
as mysql.connector.version.
"""
VERSION = (8, 0, 5, 'b', 1)
if VERSION[3]:
    if VERSION[4]:
        VERSION_TEXT = ('{0}.{1}.{2}{3}{4}'.format)(*VERSION)
else:
    VERSION_TEXT = ('{0}.{1}.{2}'.format)(*VERSION[0:3])
VERSION_EXTRA = 'dmr'
LICENSE = 'GPLv2 with FOSS License Exception'
EDITION = ''