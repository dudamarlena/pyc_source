# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.5/dist-packages/netana/equations.py
# Compiled at: 2014-10-07 19:08:18
# Size of source mod 2**32: 1514 bytes
from griddialog import *
from wequ import wequ
import pickle
from tkinter.messagebox import showerror

class Equations:

    def __init__(self, parent):
        self.parent = parent

    def getequ(self):
        if os.path.exists(self.EquFileName):
            self.RestoreEquations()
            dig = GridDialog(self.parent, self.Mat, collab=self.AnalType)
            self.cleanup(dig)
        else:
            if os.path.exists(self.NetFileName):
                self.Mat = wequ(self.NetFileName)
                dig = GridDialog(self.parent, self.Mat, collab=self.AnalType)
                self.cleanup(dig)
            else:
                dig = GridDialog(self.parent, size=self.Nodes, collab=self.AnalType)
                self.cleanup(dig)

    def cleanup(self, dig):
        if dig.status == 'Save':
            self.Mat = dig.get()
            self.SaveEquations()
        if dig.top:
            dig.top.destroy()

    def SaveEquations(self):
        if len(self.Mat) > 1:
            pickle.dump(self.Mat, open(self.EquFileName, 'wb'))

    def RestoreEquations(self):
        if os.path.exists(self.EquFileName):
            self.Mat = pickle.load(open(self.EquFileName, 'rb'))


if __name__ == '__main__':
    import os, pickle
    from tkinter import *
    root = Tk()
    os.chdir('/home/jim/test')
    eq = Equations(root)
    eq.Mat = [[1, 2, 3, 4],
     [
      5, 6, 7, 8],
     [
      9, 10, 11, 12],
     [
      13, 14, 15, 16]]
    eq.AnalType = 'Node'
    eq.Nodes = 4
    eq.EquFileName = '/home/jim/test/Wein_Bridge.equ'
    eq.EquFileName = ''
    eq.getequ()
    print('Mat = {}'.format(eq.Mat))
    root.mainloop()