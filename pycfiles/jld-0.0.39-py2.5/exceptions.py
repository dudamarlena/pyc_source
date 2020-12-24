# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Documents and Settings\Jean-Lou Dupont\My Documents\workspace_gae\jldupont\trunk\libs\python\jld\jld\tools\exceptions.py
# Compiled at: 2009-01-17 16:51:26
"""
    @author: Jean-Lou Dupont
"""
__author__ = 'Jean-Lou Dupont'
__version__ = '$Id: exceptions.py 825 2009-01-17 21:53:29Z JeanLou.Dupont $'

class ErrorMissingDependency(Exception):

    def __init__(self, msg, params=None):
        Exception.__init__(self, msg)
        self.msg = msg
        self.params = params