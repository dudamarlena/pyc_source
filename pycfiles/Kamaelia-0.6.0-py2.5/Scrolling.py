# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/Kamaelia/Support/Tk/Scrolling.py
# Compiled at: 2008-10-19 12:19:52
"""
A couple of experimental classes to support some useful basic user interface elements
One of these is a scrolling menu (!)
"""
from Tkinter import *

def _defaultCallback(*args):
    pass


class ScrollingList:

    def __init__(self, master, callback=_defaultCallback):
        scrollbar = Scrollbar(master, orient=VERTICAL)
        self.listbox = Listbox(master, yscrollcommand=scrollbar.set)
        self.listbox.bind('<ButtonRelease-1>', self.lbcallback)
        scrollbar.config(command=self.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        self.listbox.pack(side=LEFT, fill=BOTH, expand=1)
        self.insert = self.listbox.insert
        self.cb = callback

    def yview(self, *args):
        apply(self.listbox.yview, args)

    def lbcallback(self, *args):
        self.cb(self.listbox.curselection(), self.listbox.selection_get())


class ScrollingMenu(Frame):

    def __init__(self, parent, items, command=_defaultCallback, width=0, minwidth=10, maxwidth=1000):
        Frame.__init__(self, parent, relief=RAISED, borderwidth=2)
        self.callback = command
        self.SelectedItem = 0
        self.SelectedItemText = items[0]
        if width is 0:
            width = 0
            for item in items:
                width = max(len(item), width)

            if width < minwidth:
                width = minwidth
            if width > maxwidth:
                width = maxwidth
        self.button = Button(self, text=self.SelectedItemText, width=width)
        self.button.pack(side=LEFT)
        self.LB_Container = Toplevel()
        self.list = ScrollingList(self.LB_Container, self.ListboxClicked)
        for item in items:
            self.list.insert(END, item)

        self.items = items
        self.button.bind('<1>', self.buttonClicked)
        self.button.bind('<5>', self.scrollDown)
        self.button.bind('<4>', self.scrollUp)
        self.LB_Container.bind('<Escape>', self.hideMenu)
        self.DropDownVisible = None
        self.hideMenu()
        return

    def scrollDown(self, *args):
        self.SelectedItem += 1
        if self.SelectedItem >= len(self.items):
            self.SelectedItem = len(self.items) - 1
        self.SelectedItemText = self.items[self.SelectedItem]
        self.itemSelected(self.SelectedItem, self.SelectedItemText)

    def scrollUp(self, *args):
        self.SelectedItem -= 1
        if self.SelectedItem < 0:
            self.SelectedItem = 0
        self.SelectedItemText = self.items[self.SelectedItem]
        self.itemSelected(self.SelectedItem, self.SelectedItemText)

    def itemSelected(self, index, selection):
        self.SelectedItem = index
        self.SelectedItemText = selection
        self.button.configure(text=selection)
        self.callback(self.SelectedItem, self.SelectedItemText)

    def ListboxClicked(self, index, selection):
        self.hideMenu()
        self.itemSelected(int(index[0]), selection)

    def hideMenu(self, *args):
        self.LB_Container.withdraw()
        self.LB_Container.overrideredirect(1)
        self.DropDownVisible = False

    def buttonClicked(self, *args):
        if self.DropDownVisible:
            self.hideMenu(*args)
        else:
            self.showMenu(*args)

    def showMenu(self, *args):
        redirect = self.LB_Container.overrideredirect()
        if not redirect:
            self.LB_Container.overrideredirect(1)
        self.LB_Container.deiconify()
        x = self.button.winfo_rootx()
        y = self.button.winfo_rooty() + self.button.winfo_height()
        w = self.button.winfo_width()
        h = self.list.listbox.winfo_height()
        sh = self.winfo_screenheight()
        if y + h > sh and y > sh / 2:
            y = self.button.winfo_rooty() - h
        self.LB_Container.geometry('%dx%d+%d+%d' % (w, 100, x, y))
        self.LB_Container.focus()
        self.DropDownVisible = True


if __name__ == '__main__':

    def TracedCallback(tag):

        def theCallback(*args):
            print 'Callback', tag, 'args', args

        return theCallback


    root = Tk()
    x = ScrollingMenu(root, ['one', 'two', 'three', 'four'] * 20, callback=TracedCallback('One'))
    x.pack(side=LEFT)
    y = ScrollingMenu(root, ['one', 'two', 'three', 'four'] * 20, callback=TracedCallback('Two'))
    y.pack(side=LEFT)
    mainloop()