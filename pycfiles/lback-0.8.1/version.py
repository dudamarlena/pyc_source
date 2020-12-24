# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: mysql\connector\version.pyc
# Compiled at: 2014-07-26 22:44:24
"""MySQL Connector/Python version information

The file version.py gets installed and is available after installation
as mysql.connector.version.
"""
VERSION = (1, 2, 0, 'a', 1)
if VERSION[3] and VERSION[4]:
    VERSION_TEXT = ('{0}.{1}.{2}{3}{4}').format(*VERSION)
else:
    VERSION_TEXT = ('{0}.{1}.{2}').format(*VERSION[0:3])
LICENSE = 'GPLv2 with FOSS License Exception'
EDITION = ''