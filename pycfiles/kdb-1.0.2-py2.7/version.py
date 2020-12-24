# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/kdb/version.py
# Compiled at: 2014-04-26 11:22:07
"""Version Module

So we only have to maintain version information in one place!
"""
version_info = (1, 0, 2)
version = ('.').join(map(str, version_info))