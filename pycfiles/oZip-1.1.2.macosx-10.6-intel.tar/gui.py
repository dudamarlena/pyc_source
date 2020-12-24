# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages/oZip/gui.py
# Compiled at: 2014-08-30 09:16:39
from Tkinter import Tk, Frame, BOTH, Checkbutton, Listbox, END
import tkFileDialog
from ttk import Button, Style
import tkMessageBox as box
from Queue import Queue
from threading import Thread
from queue import runPool
import ntpath

class MainWindow(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent, background='white')
        self.parent = parent
        self.files = []
        self.lb = None
        self.should_decompress = False
        self.initUI()
        self.update_idletasks()
        return

    def initUI(self):
        """ Create the UI """
        self.parent.title('oZip')
        self.pack(fill=BOTH, expand=1)
        addFileButton = Button(self, text='Add File', command=self.onOpen)
        addFileButton.place(x=225, y=30)
        goButton = Button(self, text='Go', command=self.onClick)
        goButton.place(x=225, y=100)
        quitButton = Button(self, text='Quit', command=self.quit)
        quitButton.place(x=225, y=160)
        self.cb = Checkbutton(self, text='Should decompress', command=self.checkboxClick)
        self.cb.place(x=20, y=195)
        lb = Listbox(self)
        self.lb = lb
        lb.place(x=20, y=20)

    def checkboxClick(self):
        """ Update the variable that stores the action that will be done on the files """
        self.cb.update_idletasks()
        self.should_decompress = not self.should_decompress

    def onClick(self):
        """ 'Go' button pressed """
        err_q = Queue()
        worker = Thread(target=runPool, args=(self.files, err_q, self.should_decompress))
        worker.setDaemon(True)
        worker.start()
        while True:
            var = err_q.get()
            if isinstance(var, tuple):
                self.showError(var[0], var[1])
            elif isinstance(var, str):
                break
            err_q.task_done()

        box.showinfo('Done', 'Processing completed.')
        self.quit()

    def showError(self, filename, error_msg):
        """ Show an error msg if needed """
        box.showerror('Error on file %s' % filename, error_msg)

    def onOpen(self):
        """ 'Add File' button was clicked """
        selected_files = tkFileDialog.askopenfilenames()
        for path in selected_files:
            self.files.append(path)
            self.lb.insert(END, ntpath.split(path)[(-1)])
            self.lb.update_idletasks()


def main():
    """ Main GUI Function """
    root = Tk()
    root.geometry('350x225+300+300')
    app = MainWindow(root)
    root.mainloop()


if __name__ == '__main__':
    main()