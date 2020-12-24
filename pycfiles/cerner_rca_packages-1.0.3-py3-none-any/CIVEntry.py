# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/gui/cGui/widgets/compounds/CIVEntry.py
# Compiled at: 2012-04-25 01:07:44
__doc__ = '\nCreated on Apr 24, 2012\n\n@author: Anarchee\n'
import Tkinter
from gui.cGui.widgets.CEntry import CEntry

class CIVEntry(CEntry):
    """
    Just an Extension of Tkinter's Entry object for Cernent/Cerno that contains an intial text value. This 
    widget is specialized for the email frame because it makes up of the Tkinter.StringVars used by the EmailItemWrapper class.
    """

    def __init__(self, master, text, emailFrame, **cnf):
        """
        Creates a new CIVEntry instance. 
        
        Vars:
            
            master: The master widget this widget is attached to.
            
            text: The initial text. 
            
            emailFrame: The CEmailFrame this widget is associated with. 
            
        """
        CEntry.__init__(self, master)
        self.defaultText = text
        self.emailFrame = emailFrame
        self.textvar = Tkinter.StringVar()
        self.textvar.set('...')
        self.configure(textvariable=self.textvar)
        self.bind('<Button-1>', self.firstClick)
        self.bind('<FocusOut>', self.focusOut)

    def firstClick(self, other):
        """
        """
        if self.textvar.get() == self.defaultText and self['state'] == Tkinter.NORMAL:
            self.textvar.set('')

    def focusOut(self, event):
        """
        """
        if self.textvar.get() == '':
            self.config(self.textvar.set(self.defaultText))
        self.emailFrame._saveEntry()

    def setTextVar(self, textVar):
        """
        Sets the input textvar as the active textvar for the text of the textbox. 
        
        Agrs:
        
            textVar: the new current active textvar. 
        
        """
        self.textvar = textVar
        self.configure(textvariable=self.textvar)