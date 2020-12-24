# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/gui/cGui/widgets/CInitialValueEntry.py
# Compiled at: 2012-04-30 15:56:19
__doc__ = '\n.. module:: CInitialValueEntry\n   :platform: Unix\n   :synopsis: This module defines the CInitialValueEntry class   \n\n.. moduleauthor:: Daniel Chee\n'
import Tkinter
from gui.cGui.config.GuiConfig import getBackgroundColor

class CInitialValueEntry(Tkinter.Entry):
    """
    Just an Extension of Tkinter's Entry object for Cernent/Cerno that has initial text that 
    is cleared away after the first click. 
    """
    FIRST = True

    def __init__(self, master, text, **cnf):
        """
        Creates a new CInitialValueEntry with the given initial text. 
        
        Args:
        
            text: The initial text.
        """
        Tkinter.Entry.__init__(self, master, cnf)
        self.insert(0, text)
        self.bind('<Button-1>', self.firstClick)
        self.config(highlightbackground=getBackgroundColor())

    def firstClick(self, other):
        if self.FIRST == True and self['state'] == Tkinter.NORMAL:
            self.delete(0, Tkinter.END)
            self.FIRST = False