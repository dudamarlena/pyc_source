# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.5/dist-packages/netana/griddialog.py
# Compiled at: 2014-10-07 19:10:06
# Size of source mod 2**32: 3752 bytes
from tkinter import *
from tkinter import ttk
import os

class GridDialog:

    def __init__(self, parent, matrix=None, size=0, title='Grid Dialog', label='Equation Matrix', rowlab='Equ', collab='Node'):
        self.top = Toplevel(parent)
        self.top.title(title)
        self.top.transient(parent)
        self.top.geometry('+150+250')
        self.top.grab_set()
        self.parent = parent
        self.result = None
        self.entdict = {}
        if matrix == None:
            self.matrix = None
            self.rows = size
            self.cols = size
        else:
            self.matrix = matrix
            self.rows = len(matrix)
            self.cols = len(matrix[0])
        self.rowlab = rowlab
        self.collab = collab
        self.top.protocol('WM_DELETE_WINDOW', self.cancel)
        self.initial_focus = self.body(label)
        self.parent.wait_window(self.top)

    def body(self, label):
        f1 = ttk.Frame(self.top, borderwidth=2, relief=GROOVE)
        ttk.Label(f1, text=label, font='20').pack(side=TOP, padx=10, pady=10)
        f1.pack()
        colwidth = 12
        f2 = ttk.Frame(self.top, borderwidth=2, relief=GROOVE)
        ttk.Label(f2, text=None, width=5).grid(row=0, column=0, sticky=W, padx=5, pady=5)
        for c in range(self.cols):
            lab = self.collab + ' ' + str(c + 1)
            ttk.Label(f2, width=colwidth, text=lab).grid(row=0, column=c + 1, sticky=W, pady=5)

        f2.pack()
        self.entdict = {}
        f3 = ttk.Frame(self.top, borderwidth=2, relief=GROOVE)
        for r in range(self.rows):
            lab = self.rowlab + ' ' + str(r + 1)
            ttk.Label(f3, text=lab).grid(row=r, column=0, sticky=W, pady=5)
            for c in range(self.cols):
                if r == c:
                    bgcolor = 'Gray80'
                else:
                    bgcolor = 'White'
                e = StringVar()
                ent = ttk.Entry(f3, width=12, textvariable=e, background=bgcolor).grid(row=r, column=c + 1, sticky=W, pady=5)
                e.set('0')
                self.entdict[(r, c)] = e

        f3.pack()
        f4 = ttk.Frame(self.top, borderwidth=2, relief=GROOVE)
        ttk.Button(f4, text='Save', command=self.save).pack(side=LEFT, padx=5, pady=5)
        cb = ttk.Button(f4, text='Cancel', command=self.cancel).pack(side=LEFT, padx=5, pady=5)
        self.top.bind('<Escape>', self.cancel)
        f4.pack(anchor=W)
        if self.matrix != None:
            self._set(self.matrix)

    def _set(self, mat):
        """Internal Method Only: to set entries in the GridDialog it
                uses the Matrix passed to this method."""
        for r in range(len(mat)):
            for c in range(len(mat[0])):
                f = self.entdict[(r, c)]
                f.set(mat[r][c])

    def get(self):
        """Method returns matrix (lists of lists) from
                the grid dialog"""
        mat = []
        for r in range(self.rows):
            colmat = []
            for c in range(self.cols):
                f = self.entdict[(r, c)]
                equ = f.get()
                colmat.append(equ)

            mat.append(colmat)

        return mat

    def save(self, event=None):
        self.top.withdraw()
        self.top.update_idletasks()
        self.parent.focus_set()
        self.top.destroy()
        self.status = 'Save'

    def cancel(self, event=None):
        self.parent.focus_set()
        self.top.destroy()
        self.status = 'Cancel'


if __name__ == '__main__':
    root = Tk()
    root.title('Root')
    root.geometry('+100+200')
    mat = [
     [
      0, 1, 2, 3, 4],
     [
      5, 6, 7, 8, 9],
     [
      10, 11, 12, 13, 14],
     [
      15, 16, 17, 18, 19],
     [
      20, 21, 22, 23, 24]]
    dig = GridDialog(root, size=len(mat))
    print('status = {}'.format(dig.status))
    new_mat = dig.get()
    print('new_mat = {}'.format(new_mat))
    dig.top.destroy()
    dig = GridDialog(root, mat)
    print('status = {}'.format(dig.status))
    new_mat = dig.get()
    print('new_mat = {}'.format(new_mat))
    dig.top.destroy()
    root.mainloop()