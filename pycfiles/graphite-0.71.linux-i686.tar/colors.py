# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.5/site-packages/graphite/colors.py
# Compiled at: 2003-12-28 18:59:49
"""This is a compatibility kluge to let you say

import colors
 ... colors.black ...

when using either PIDDLE or SPING.
"""
try:
    from sping.colors import *
except:
    from piddle import *