# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\jld\backup\delicious_messages.py
# Compiled at: 2009-01-13 14:40:52
""" Messages interface for Delicious Backup
"""
__author__ = 'Jean-Lou Dupont'
__version__ = '$Id: delicious_messages.py 795 2009-01-13 19:42:53Z JeanLou.Dupont $'
import os
from jld.tools.messages import Messages

class Delicious_Messages(Messages):
    filepath = os.path.dirname(os.path.abspath(__file__)) + os.sep + 'delicious_messages.yaml'

    def __init__(self):
        Messages.__init__(self, self.filepath)