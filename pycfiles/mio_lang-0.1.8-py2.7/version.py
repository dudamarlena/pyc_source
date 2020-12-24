# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/prologic/work/mio/mio/version.py
# Compiled at: 2013-12-24 00:31:09
"""Version Module

So we only have to maintain version information in one place!
"""
version_info = (0, 1, 8)
version = ('.').join(map(str, version_info))