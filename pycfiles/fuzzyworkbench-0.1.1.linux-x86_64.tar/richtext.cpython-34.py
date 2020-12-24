# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.4/dist-packages/fuzzyworkbench/richtext.py
# Compiled at: 2015-10-01 12:54:48
# Size of source mod 2**32: 2532 bytes
import tkinter as tk
from tkinter import font

class RuleRichText(tk.Text):
    __doc__ = 'RichText for Rules editing\n    \n    Adapted from: http://stackoverflow.com/questions/3781670/\n    '

    def __init__(self, *args, **kwargs):
        tk.Text.__init__(self, *args, **kwargs)
        self._baseFont = font.Font(family='Helvetica', size=14)
        self._boldFont = font.Font(weight='bold', size=14)
        self.config(font=self._baseFont)
        self._regex = '(^if | then | and | or | is )'
        self.tag_configure('keyword', foreground='#a00093', font=self._boldFont)
        self.tag_configure('error', background='#ffa0a0')
        self.bind('<Control-c>', self._copy)
        self.bind('<Control-x>', self._cut)
        self.bind('<Control-v>', self._paste)

    def _copy(self, event=None):
        self.clipboard_clear()
        text = self.get('sel.first', 'sel.last')
        self.clipboard_append(text)

    def _cut(self, event):
        self.copy()
        self.delete('sel.first', 'sel.last')

    def _paste(self, event):
        text = self.selection_get(selection='CLIPBOARD')
        self.insert('insert', text)

    def clear_errors(self):
        self.tag_remove('error', '1.0', tk.END)

    def highlight_error(self, line):
        self.tag_add('error', '%d.0' % (line + 1), '%d.end+1c' % (line + 1))

    def highlight_keywords(self):
        self.tag_remove('keyword', '1.0', tk.END)
        self.highlight_pattern(self._regex, 'keyword', regexp=True)

    def highlight_pattern(self, pattern, tag, start='1.0', end='end', regexp=False):
        """Apply the given tag to all text that matches the given pattern

        If 'regexp' is set to True, pattern will be treated as a regular
        expression.
        
        See: http://stackoverflow.com/questions/3781670/
        """
        start = self.index(start)
        end = self.index(end)
        self.mark_set('matchStart', start)
        self.mark_set('matchEnd', start)
        self.mark_set('searchLimit', end)
        count = tk.IntVar()
        while True:
            index = self.search(pattern, 'matchEnd', 'searchLimit', count=count, regexp=regexp, nocase=1)
            if index == '':
                break
            self.mark_set('matchStart', index)
            self.mark_set('matchEnd', '%s+%sc' % (index, count.get()))
            self.tag_add(tag, 'matchStart', 'matchEnd')