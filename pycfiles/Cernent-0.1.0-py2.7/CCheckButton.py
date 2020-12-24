# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/gui/cGui/widgets/CCheckButton.py
# Compiled at: 2012-04-18 12:17:46
"""
Created on Mar 13, 2012

@author: bkraus
"""
import Tkinter
from gui.cGui.config.GuiConfig import getBackgroundColor

class CCheckButton(Tkinter.Checkbutton):
    """
    Just a simple extension of Tkinter.Checkbutton for Cernent.
    """

    def __init__(self, master, **cnf):
        Tkinter.Checkbutton.__init__(self, master, cnf)
        self.config(highlightbackground=getBackgroundColor(), background=getBackgroundColor())