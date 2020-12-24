# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/Infinidat/infi.pyutils/tests/test_utils.py
# Compiled at: 2016-09-14 06:55:36
import platform
if platform.python_version() < '2.7':
    from unittest2 import TestCase
else:
    from unittest import TestCase