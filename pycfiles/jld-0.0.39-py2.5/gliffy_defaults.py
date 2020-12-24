# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\jld\backup\gliffy_defaults.py
# Compiled at: 2009-01-13 14:40:52
""" Gliffy Backup utility
    @author: Jean-Lou Dupont
"""
__author__ = 'Jean-Lou Dupont'
__version__ = '$Id: gliffy_defaults.py 795 2009-01-13 19:42:53Z JeanLou.Dupont $'
import os, jld.tools.defaults as Defaults

class Gliffy_Defaults(Defaults.Defaults):
    _path = os.path.dirname(__file__) + os.sep + 'gliffy_defaults.yaml'

    def __init__(self):
        Defaults.Defaults.__init__(self)