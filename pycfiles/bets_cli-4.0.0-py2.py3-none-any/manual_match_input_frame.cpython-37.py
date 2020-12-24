# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\PROJECT_HOME\bets-cli\src\bets\ui\matches_tab\manual_match_input_frame.py
# Compiled at: 2019-03-27 01:38:28
# Size of source mod 2**32: 2968 bytes
from tkinter import DoubleVar, StringVar, messagebox, EW, NSEW
from tkinter.ttk import Button, Entry, Label, LabelFrame
from typing import Tuple, Optional
from bets.model.matches import Matches
from bets.ui.constants import PAD_X, PAD_Y, W_MATCH_RATIO, W_MATCH_TITLE
from bets.utils import log

class ManualMatchInputFrame(LabelFrame):
    title_input: Entry
    ratio_1_input: Entry
    ratio_x_input: Entry
    ratio_2_input: Entry

    def __init__(self, parent, matches, column=1, row=1):
        super().__init__(parent, text=' Manual input ')
        self._matches = matches
        self._var_title = StringVar()
        self._var_ratio_1 = DoubleVar()
        self._var_ratio_x = DoubleVar()
        self._var_ratio_2 = DoubleVar()
        self.grid(column=column, row=row, sticky=NSEW, padx=PAD_X, pady=PAD_Y)
        self.create_widgets()

    def create_widgets(self):
        Label(self, text='Title:').grid(column=0, row=0)
        Label(self, text='1:').grid(column=0, row=1)
        Label(self, text='X:').grid(column=0, row=2)
        Label(self, text='2:').grid(column=0, row=3)
        self.title_input = Entry(self, width=W_MATCH_TITLE, textvariable=(self._var_title))
        self.title_input.grid(column=1, row=0, columnspan=2)
        self.title_input.focus()
        self.ratio_1_input = Entry(self, width=W_MATCH_RATIO, textvariable=(self._var_ratio_1))
        self.ratio_1_input.grid(column=1, row=1)
        self.ratio_x_input = Entry(self, width=W_MATCH_RATIO, textvariable=(self._var_ratio_x))
        self.ratio_x_input.grid(column=1, row=2)
        self.ratio_2_input = Entry(self, width=W_MATCH_RATIO, textvariable=(self._var_ratio_2))
        self.ratio_2_input.grid(column=1, row=3)
        Button(self, text='Add', command=(self._add_match)).grid(column=2, row=1)
        Button(self, text='Clear', command=(self._clear_inputs)).grid(column=2, row=2)
        Button(self, text='Clear all', command=(self._matches.clear)).grid(column=2, row=3)
        for child in self.winfo_children():
            child.grid_configure(padx=PAD_X, pady=PAD_Y, sticky=EW)

    def _clear_inputs(self):
        self._var_title.set('')
        self._var_ratio_1.set(0.0)
        self._var_ratio_x.set(0.0)
        self._var_ratio_2.set(0.0)
        self.title_input.focus()

    def _get_values(self) -> Optional[Tuple[(str, float, float, float)]]:
        try:
            return (
             self._var_title.get(), self._var_ratio_1.get(), self._var_ratio_x.get(), self._var_ratio_2.get())
        except Exception as ex:
            try:
                log.debug(f"Exception while getting manual matches input values: {ex}")
                messagebox.showerror('Invalid input', 'Try again with different values!')
                return
            finally:
                ex = None
                del ex

    def _add_match(self):
        match_details = self._get_values()
        if match_details:
            (self._matches.add_match)(*match_details)
        self._clear_inputs()