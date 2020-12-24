# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\jld\tools\debug.py
# Compiled at: 2009-01-13 14:40:52
""" Debug related tools
    @author: Jean-Lou Dupont
"""
__author__ = 'Jean-Lou Dupont'
__version__ = '$Id: debug.py 795 2009-01-13 19:42:53Z JeanLou.Dupont $'
import inspect

def lineno():
    """Returns the current line number"""
    return inspect.currentframe().f_back.f_lineno