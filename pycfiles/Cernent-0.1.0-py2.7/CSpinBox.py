# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/gui/cGui/widgets/CSpinBox.py
# Compiled at: 2012-04-13 00:17:33
"""
Created on Mar 13, 2012

@author: bkraus
"""
from Tkinter import Spinbox
from gui.cGui.config.GuiConfig import getBackgroundColor

class CSpinBox(Spinbox):
    """
    Extension of Tkinter.Spinbox
    """

    def __init__(self, master, **cnf):
        Spinbox.__init__(self, master, cnf)
        self.config(highlightbackground=getBackgroundColor())