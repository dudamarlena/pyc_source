# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/noval/calltip.py
# Compiled at: 2019-08-18 05:01:23
# Size of source mod 2**32: 2971 bytes
from noval import GetApp, _
import tkinter as tk
from tkinter import ttk

class CalltipBox(ttk.Frame):

    def __init__(self, text):
        ttk.Frame.__init__(self, master=text)
        self.text = text
        self.doc_label = ttk.Label(master=self, text='Aaappiiiii')
        self.doc_label.pack(fill='both', expand=1)
        self.text.bind('<1>', self.on_text_click)
        self.doc_label.bind('<Escape>', self._close)

    def _present_completions(self, completions, replaceLen):
        self.completions = completions
        self._typedlen = replaceLen
        if len(completions) == 0:
            self._close()
        else:
            if len(completions) == 1:
                self._insert_completion(completions[0])
                self._close()
            else:
                self._show_box(completions)

    def _show_box(self, pos, docstring):
        if not docstring:
            return
        if not self._is_visible():
            height = 100
            text_box_x, text_box_y, _, text_box_height = self.text.bbox('%d.%d' % (pos[0], pos[1]))
            space_below = self.master.winfo_height() - text_box_y - text_box_height
            space_above = text_box_y
            if space_below >= height or space_below > space_above:
                height = min(height, space_below)
                y = text_box_y + text_box_height
            else:
                height = min(height, space_above)
                y = text_box_y - height
            self.place(x=text_box_x, y=y)
            self._update_doc(docstring)

    def _update_doc(self, docstring):
        if docstring:
            self.doc_label['text'] = docstring
        else:
            self.doc_label['text'] = ''

    def _is_visible(self):
        return self.winfo_ismapped()

    def _get_position(self):
        return map(int, self.text.index('insert').split('.'))

    def _on_text_keypress(self, event=None):
        if not self._is_visible():
            return
        if event.keysym == 'Escape':
            self._close()
            return 'break'
        if event.keysym in ('Return', 'KP_Enter', 'Tab'):
            assert self.listbox.size() > 0
            self._insert_current_selection()
            return 'break'

    def _close(self, event=None):
        self.place_forget()
        self.text.focus_set()

    def on_text_click(self, event=None):
        if self._is_visible():
            self._close()