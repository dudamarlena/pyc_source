# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/sss/exceptions.py
# Compiled at: 2010-12-03 16:29:41
"""Exception classes for Simple Scrum System"""

class EmptyBurndownError(Exception):
    """Occurring when you want to draw a burndown chart with empty data"""
    pass