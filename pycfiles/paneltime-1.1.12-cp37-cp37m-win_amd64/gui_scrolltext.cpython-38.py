# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: \\ad.uit.no\uit\data\esi000data\dokumenter\forskning\papers\paneltime\paneltime\paneltime\gui\gui_scrolltext.py
# Compiled at: 2020-01-13 14:25:19
# Size of source mod 2**32: 5929 bytes
import tkinter as tk, keyword, numpy as np, re
font0 = 'Courier 10'
ret_chr = ['\r', '\n']

class ScrollText(tk.Frame):

    def __init__(self, master, readonly=False, text=None, format_text=True):
        tk.Frame.__init__(self, master)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        xscrollbar = tk.Scrollbar(self, orient='horizontal')
        yscrollbar = tk.Scrollbar(self)
        self.text_box = CustomText(self, wrap=(tk.NONE), xscrollcommand=(xscrollbar.set), yscrollcommand=(yscrollbar.set), undo=True, format_text=format_text)
        xscrollbar.config(command=(self.text_box.xview))
        yscrollbar.config(command=(self.text_box.yview))
        xscrollbar.grid(row=1, column=0, sticky='ew')
        yscrollbar.grid(row=0, column=1, sticky='ns')
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

    def insert(self, index1, chars, index2=None):
        if self.readonly:
            self.text_box.configure(state='normal')
        if index2 is not None:
            self.text_box.delete(index1, index2)
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

    def __init__(self, master, wrap, xscrollcommand, yscrollcommand, undo, format_text=True):
        font = 'Courier'
        size = 12
        tk.Text.__init__(self, master, wrap=wrap, xscrollcommand=xscrollcommand,
          yscrollcommand=yscrollcommand,
          undo=undo)
        self.configure(font=(font, size, 'normal'))
        self.bind('<KeyRelease>', self.changed)
        self.tag_configure('quote', foreground='dark red')
        self.tag_configure('keyword', foreground='#0a00bf')
        self.tag_configure('comment', foreground='#00a619')
        self.tag_configure('definition', foreground='#008a5a')
        self.tag_configure('bold', font=(font, size, 'bold'))
        self.tag_configure('normal', font=(font, size, 'normal'))
        self.tag_configure('black', foreground='black')
        self.define_keywords()
        self.format_text = format_text

    def define_keywords(self):
        kwlist = np.array(keyword.kwlist)
        kwlensrt = np.array([len(i) for i in keyword.kwlist]).argsort()
        self.kwrds = list(kwlist[kwlensrt])
        self.kwrds.append('print')

    def changed(self, event=None):
        if not self.format_text:
            return
        if event is not None:
            if event.keycode == 65 or event.keycode == 17:
                return
        for tag in self.tag_names():
            self.tag_remove(tag, '1.0', 'end')
        else:
            self.highlight_pattern('\\"(.*?)\\"', 'quote')
            self.highlight_pattern("'(.*?)'", 'quote')
            self.highlight_pattern('def (.*?)\\(', 'definition', addstart=4, subtractend=1, tag2='bold')
            self.highlight_pattern('\\"\\"\\"(.*?)\\"\\"\\"', 'quote')
            self.highlight_pattern_multiline('\\"\\"\\"([\\s\\S]*?)\\"\\"\\"', 'quote')
            self.highlight_pattern('#(.*?)\\r', 'comment', end='end-1c')
            self.highlight_pattern('#(.*?)\\n', 'comment', end='end-1c')
            for i in self.kwrds:
                self.highlight_pattern(('\\m(%s)\\M' % (i,)), 'keyword', tag2='bold')

    def highlight_pattern(self, pattern, tag, start='1.0', end='end', regexp=True, tag2=None, addstart=0, subtractend=0):
        indicies = self.search_pattern(pattern, start=start, end=end, regexp=regexp, addstart=addstart, subtractend=subtractend)
        if len(indicies) == 0:
            return
        for index1, index2 in indicies:
            self.tag_add(tag, index1, index2)
            if tag2 is not None:
                self.tag_add(tag2, index1, index2)

    def highlight_pattern_multiline(self, pattern, tag, start='1.0', end='end', regexp=True, tag2=None, addstart=0, subtractend=0):
        s = self.get('1.0', tk.END)
        start = 0
        while True:
            m = re.search(pattern, s[start:])
            if m is None:
                break
            index1 = self.pos_to_index(m.start() + start, s)
            index2 = self.pos_to_index(m.end() + start, s)
            self.tag_add(tag, index1, index2)
            if tag2 is not None:
                self.tag_add(tag2, index1, index2)
            start = m.end() + start

    def search_pattern(self, pattern, start='1.0', end='end', regexp=True, addstart=0, subtractend=0):
        start = self.index(start)
        end = self.index(end)
        self.mark_set('matchStart', start)
        self.mark_set('matchEnd', start)
        self.mark_set('searchLimit', end)
        count = tk.IntVar()
        indicies = []
        while True:
            index1 = self.search(pattern, 'matchEnd', 'searchLimit', count=count,
              regexp=regexp)
            if index1 == '':
                break
            n = count.get() - subtractend
            if n <= 0:
                break
            index2 = '%s+%sc' % (index1, n)
            if addstart > 0:
                index1 = f"{index1}+{addstart}c"
            self.mark_set('matchStart', index1)
            self.mark_set('matchEnd', index2)
            indicies.append((index1, index2))

        return indicies

    def pos_to_index(self, pos, string):
        s = str(string[:pos + 1])
        if pos + 1 > len(s):
            pos = len(s) - 1
        lines = s.split('\n')
        if len(lines) == 1:
            return f"1.{len(s)}"
        chars = lines[(-1)]
        index = f"{len(lines)}.{len(chars)}"
        return index