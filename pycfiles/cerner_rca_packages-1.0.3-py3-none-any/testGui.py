# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/gui/test/testGui.py
# Compiled at: 2012-04-13 00:17:32
__doc__ = '\nCreated on Feb 24, 2012\n\n@author: bkraus\n'
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