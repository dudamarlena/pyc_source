# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/gui/cGui/widgets/CListBox.py
# Compiled at: 2012-04-13 00:17:33
"""
Created on Feb 27, 2012

@author: bkraus
"""
import Tkinter
from gui.cGui.config.GuiConfig import getBackgroundColor

class CListBox(Tkinter.Listbox):
    """
    An extension of Tkinter's ListBox for Cernent/Cerno
    """

    def __init__(self, master, **cnf):
        Tkinter.Listbox.__init__(self, master, cnf)
        self.config(highlightbackground=getBackgroundColor())