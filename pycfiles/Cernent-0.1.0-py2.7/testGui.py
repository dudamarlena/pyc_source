# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/gui/test/testGui.py
# Compiled at: 2012-04-13 00:17:32
"""
Created on Feb 24, 2012

@author: bkraus
"""
import Tkinter

class testGui(Tkinter.Tk):

    def __init__(self, parent):
        Tkinter.Tk.__init__(self, parent)
        self.parent = parent
        self.initialize()

    def initialize(self):
        self.makeButton()

    def makeButton(self):
        buttonFrame = Tkinter.Frame(self, background='black')
        doButton = Tkinter.Button(buttonFrame, text='Click ME!', command=self.buttonClick)
        doButton.grid(row=0, column=0)
        buttonFrame.grid(row=0, column=0, columnspan=1)

    def buttonClick(self):
        print 'Heyo!'


def main():
    app = testGui(None)
    app.title('My little gui.')
    app.mainloop()
    return


if __name__ == '__main__':
    main()