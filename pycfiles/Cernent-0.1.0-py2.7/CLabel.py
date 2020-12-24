# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/gui/cGui/widgets/CLabel.py
# Compiled at: 2012-04-13 00:17:33
"""
Created on Feb 26, 2012

@author: bkraus
"""
import Tkinter
from gui.cGui.config.GuiConfig import getLabelBackgroundColor
from gui.cGui.config.GuiConfig import getForegroundColor

class CLabel(Tkinter.Label):
    """
    Just an Extension of Tkinter's Label object for Cernent/Cerno
    """

    def __init__(self, master, **cnf):
        Tkinter.Label.__init__(self, master, cnf)
        self.config(bg=getLabelBackgroundColor(), foreground=getForegroundColor(), border=1, relief='raised')