# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: b:\forskning\papers\paneltime\paneltime\paneltime\gui\gui_scrolltext.py
# Compiled at: 2020-01-08 06:13:15
# Size of source mod 2**32: 5007 bytes
import tkinter as tk, keyword, numpy as np
font0 = 'Courier 10'
ret_chr = ['\r', '\n']

class ScrollText(tk.Frame):

    def __init__(self, window, row, readonly=False, text=None):
        tk.Frame.__init__(self, window)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        xscrollbar = tk.Scrollbar(self, orient='horizontal')
        yscrollbar = tk.Scrollbar(self)
        self.text_box = CustomText(self, wrap=(tk.NONE), xscrollcommand=(xscrollbar.set), yscrollcommand=(yscrollbar.set), undo=True)
        xscrollbar.config(command=(self.text_box.xview))
        yscrollbar.config(command=(self.text_box.yview))
        xscrollbar.grid(row=1, column=0, sticky='ew')
        yscrollbar.grid(row=0, column=1, sticky='ns')
        self.grid(row=row, column=0, sticky=(tk.NSEW))
        self.text_box.grid(row=0, column=0, sticky=(tk.NSEW))
        self.readonly = readonly
        if text is not None:
            self.replace_all(text)
        if readonly:
            self.text_box.configure(state='disabled')

    def get(self, index1, index2):
        return self.text_box.get(index1, index2)

    def get_all(self):
        return self.get('1.0', tk.END)

    def delete(self, index1, index2):
        if self.readonly:
            self.text_box.configure(state='normal')
        self.text_box.delete(index1, index2)
        if self.readonly:
            self.text_box.configure(state='disabled')

    def insert(self, index1, chars):
        if self.readonly:
            self.text_box.configure(state='normal')
        self.text_box.insert(index1, chars)
        if self.readonly:
            self.text_box.configure(state='disabled')
        self.text_box.changed()

    def write(self, chars):
        if self.readonly:
            return
        self.insert(tk.INSERT, chars)

    def see(self, index):
        self.text_box.see(index)

    def replace_all(self, string):
        if self.readonly:
            self.text_box.configure(state='normal')
        self.text_box.delete('1.0', tk.END)
        self.text_box.insert(tk.INSERT, string)
        if self.readonly:
            self.text_box.configure(state='disabled')
        self.text_box.changed()


class CustomText(tk.Text):
    __doc__ = 'A text widget with a new method, highlight_pattern()\n\n\texample:\n\n\ttext = CustomText()\n\ttext.tag_configure("red", foreground="#ff0000")\n\ttext.highlight_pattern("this should be red", "red")\n\n\tThe highlight_pattern method is a simplified python\n\tversion of the tcl code at http://wiki.tcl.tk/3246\n\t'

    def __init__(self, master, wrap, xscrollcommand, yscrollcommand, undo):
        tk.Text.__init__(self, master, wrap=wrap, xscrollcommand=xscrollcommand,
          yscrollcommand=yscrollcommand,
          undo=undo)
        self.configure(font=('Courier', 11, 'normal'))
        self.bind('<KeyRelease>', self.changed)
        self.tag_configure('quote', foreground='dark red')
        self.tag_configure('keyword', foreground='#0a00bf')
        self.tag_configure('comment', foreground='#00a619')
        self.tag_configure('definition', foreground='#46784e')
        self.tag_configure('bold', font=('Courier', 11, 'bold'))
        self.tag_configure('normal', font=('Courier', 11, 'normal'))
        self.tag_configure('black', foreground='black')
        self.define_keywords()

    def define_keywords(self):
        kwlist = np.array(keyword.kwlist)
        kwlensrt = np.array([len(i) for i in keyword.kwlist]).argsort()
        self.kwrds = list(kwlist[kwlensrt])
        self.kwrds.append('print')

    def changed(self, event=None):
        for tag in self.tag_names():
            self.tag_remove(tag, '1.0', 'end')

        self.highlight_pattern('\\"(.*?)\\"', 'quote')
        self.highlight_pattern("'(.*?)'", 'quote')
        self.highlight_pattern('def (.*?)\\(', 'definition', addstart=4, subtractend=1, tag2='bold')
        self.highlight_pattern('\\"\\"\\"(.*?)\\"\\"\\"', 'quote')
        self.highlight_pattern('#(.*?)\\r', 'comment', end='end-1c')
        self.highlight_pattern('#(.*?)\\n', 'comment', end='end-1c')
        for i in self.kwrds:
            self.highlight_pattern(('\\m(%s)\\M' % (i,)), 'keyword', tag2='bold')

    def highlight_pattern(self, pattern, tag, start='1.0', end='end', regexp=True, tag2=None, addstart=0, subtractend=0):
        """Apply the given tag to all text that matches the given pattern

                If 'regexp' is set to True, pattern will be treated as a regular
                expression according to Tcl's regular expression syntax.
                """
        start = self.index(start)
        end = self.index(end)
        self.mark_set('matchStart', start)
        self.mark_set('matchEnd', start)
        self.mark_set('searchLimit', end)
        count = tk.IntVar()
        while 1:
            index = self.search(pattern, 'matchEnd', 'searchLimit', count=count,
              regexp=regexp)
            if index == '':
                break
            n = count.get() - subtractend - addstart
            if n <= 0:
                break
            if addstart > 0:
                if n <= addstart:
                    break
                index = f"{index}+{addstart}c"
            self.mark_set('matchStart', index)
            self.mark_set('matchEnd', '%s+%sc' % (index, n))
            self.tag_add(tag, 'matchStart', 'matchEnd')
            if tag2 is not None:
                self.tag_add(tag2, 'matchStart', 'matchEnd')