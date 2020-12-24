# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/gui/cGui/widgets/CText.py
# Compiled at: 2012-04-13 00:17:33
__doc__ = '\nCreated on Feb 27, 2012\n\n@author: bkraus\n'
import Tkinter
from gui.cGui.config.GuiConfig import getBackgroundColor

class CText(Tkinter.Text):
    """
    Just an extension of Tkinter's Text object for Cernent/Cerno
    """

    def __init__(self, master, **cnf):
        Tkinter.Text.__init__(self, master, cnf)
        self.config(highlightbackground=getBackgroundColor())