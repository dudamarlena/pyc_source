# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\PROJECT_HOME\bets-cli\src\bets\ui\scenarios_tab\filter_frames.py
# Compiled at: 2019-03-26 20:17:21
# Size of source mod 2**32: 2917 bytes
import tkinter as tk
from tkinter import ttk
from typing import Tuple
from bets.model.matches import OUTCOMES, RANKS
COMBO_VALUES = RANKS + OUTCOMES

class TotalOccurrencesFilterFrame(tk.LabelFrame):

    def __init__(self, parent, max_value):
        super().__init__(parent, text=' Total occurrences range filter ')
        ttk.Label(self, text='Count of').grid(column=0, row=0)
        self.combo_box = ttk.Combobox(self, values=COMBO_VALUES, state='readonly', width=5)
        self.combo_box.grid(column=1, row=0)
        self.combo_box.current(0)
        ttk.Label(self, text='is in the range from:').grid(column=2, row=0)
        self.spin_from = ttk.Spinbox(self, from_=0, to=max_value, state='readonly', width=5)
        self.spin_from.grid(column=3, row=0)
        self.spin_from.set(0)
        ttk.Label(self, text='to:').grid(column=4, row=0)
        self.spin_to = ttk.Spinbox(self, from_=0, to=max_value, state='readonly', width=5)
        self.spin_to.grid(column=5, row=0)
        self.spin_to.set(max_value)
        self.apply_button = ttk.Button(self, text='Apply')
        self.apply_button.grid(column=6, row=0)
        for child in self.winfo_children():
            child.grid_configure(padx=4, pady=2, sticky=(tk.W))

    def get_values(self) -> Tuple[(str, int, int)]:
        return (self.combo_box.get(), int(self.spin_from.get()), int(self.spin_to.get()))


class SequentialOccurrencesFilterFrame(tk.LabelFrame):

    def __init__(self, parent, max_value):
        super().__init__(parent, text=' Sequential occurrences filter ')
        tk.Label(self, text='Allow max').grid(column=0, row=0)
        self.spin_to = ttk.Spinbox(self, from_=0, to=max_value, state='readonly', width=5)
        self.spin_to.grid(column=1, row=0)
        self.spin_to.set(max_value)
        tk.Label(self, text='occurrences of').grid(column=2, row=0)
        self.combo_box = ttk.Combobox(self, values=COMBO_VALUES, state='readonly', width=5)
        self.combo_box.grid(column=3, row=0)
        self.combo_box.current(0)
        tk.Label(self, text='in a row').grid(column=4, row=0)
        self.apply_button = ttk.Button(self, text='Apply')
        self.apply_button.grid(column=5, row=0)
        for child in self.winfo_children():
            child.grid_configure(padx=4, pady=2, sticky=(tk.W))

    def get_values(self) -> Tuple[(str, int)]:
        return (self.combo_box.get(), int(self.spin_to.get()))


def _test_from_to_frame():
    win = tk.Tk()
    frame = TotalOccurrencesFilterFrame(win, 5)
    frame.grid()
    win.mainloop()


def _test_occurrence_frame():
    win = tk.Tk()
    frame = SequentialOccurrencesFilterFrame(win, 5)
    frame.grid()
    frame2 = TotalOccurrencesFilterFrame(win, 5)
    frame2.grid()
    win.mainloop()


def main():
    _test_occurrence_frame()


if __name__ == '__main__':
    main()