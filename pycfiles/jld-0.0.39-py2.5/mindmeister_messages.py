# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Documents and Settings\Jean-Lou Dupont\My Documents\workspace_gae\jldupont\trunk\libs\python\jld\jld\backup\mindmeister_messages.py
# Compiled at: 2008-12-04 08:40:49
""" Messages interface for MindMeister
"""
__author__ = 'Jean-Lou Dupont'
__version__ = '$Id: mindmeister_messages.py 708 2008-12-04 13:40:35Z JeanLou.Dupont $'
import os
from jld.tools.messages import Messages

class MM_Messages(Messages):
    filepath = os.path.dirname(os.path.abspath(__file__)) + os.sep + 'mindmeister_messages.yaml'

    def __init__(self):
        Messages.__init__(self, self.filepath)