# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: \\ad.uit.no\uit\data\esi000data\dokumenter\forskning\papers\paneltime\paneltime\paneltime\gui\gui_sql.py
# Compiled at: 2020-01-13 06:21:40
# Size of source mod 2**32: 2884 bytes
import tkinter as tk
from multiprocessing import pool
import numpy as np
from gui import gui_scrolltext
import paneltime

class sql_query(tk.Toplevel):

    def __init__(self, window, parent):
        tk.Toplevel.__init__(self, window)
        self.geometry('%dx%d%+d%+d' % (900, 700, 100, 0))
        self.win = window
        self.parent = parent
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0)
        self.rowconfigure(1)
        self.rowconfigure(2, weight=5)
        self.rowconfigure(3)
        self.rowconfigure(4, weight=5)
        self.rowconfigure(5)
        self.name_txt = tk.StringVar()
        self.name_entry = tk.Frame(self)
        self.name_entry_lbl = tk.Label((self.name_entry), height=2, text='Name of query:', justify=(tk.LEFT))
        self.name_entry_field = tk.Entry((self.name_entry), textvariable=(self.name_txt))
        self.name_txt.set('Query 1')
        self.name_entry_lbl.pack(side=(tk.LEFT))
        self.name_entry_field.pack(side=(tk.LEFT))
        self.label_conn = tk.Label(self, height=2, text='Connection string:', anchor='sw', justify=(tk.LEFT))
        self.conn_str = gui_scrolltext.ScrollText(self)
        self.conn_str.insert('1.0', window.data.get('conn_str'))
        self.label_sql = tk.Label(self, height=2, text='SQL query:', anchor='sw', justify=(tk.LEFT))
        self.sql_str = gui_scrolltext.ScrollText(self)
        self.sql_str.insert('1.0', window.data.get('sql_str'))
        self.OK_button = tk.Button(self, height=2, text='OK', command=(self.ok_pressed))
        self.name_entry.grid(row=0, column=0, sticky='ew')
        self.label_conn.grid(row=1, column=0, sticky='ew')
        self.conn_str.grid(row=2, column=0, sticky=(tk.NSEW))
        self.label_sql.grid(row=3, column=0, sticky='ew')
        self.sql_str.grid(row=4, column=0, sticky=(tk.NSEW))
        self.OK_button.grid(row=5, column=0, sticky=(tk.NSEW))
        self.transient(window)
        self.grab_set()
        self.protocol('WM_DELETE_WINDOW', self.on_closing)

    def ok_pressed(self, event=None):
        self.win.data.dict['sql_str'] = self.sql_str.get_all()
        self.win.data.dict['conn_str'] = self.conn_str.get_all()
        exec(self.win.data.dict['conn_str'], self.win.globals, self.win.locals)
        exe_str = f'''df=load_SQL(conn,"""\n{self.win.data.dict['sql_str']}\n""")'''
        exec(exe_str, self.win.globals, self.win.locals)
        df = self.win.locals['df']
        f = self.name_txt.get()
        self.win.grab_set()
        self.win.right_tabs.data_tree.data_frames.add(f, df, exe_str, f"{self.win.data.dict['conn_str']}\n{exe_str}")
        self.win.right_tabs.data_tree.add_df_to_tree(df, f)
        self.win.insert_script()
        self.withdraw()

    def on_closing(self):
        self.win.grab_set()
        self.win.data.dict['sql_str'] = self.sql_str.get_all()
        self.win.data.dict['conn_str'] = self.conn_str.get_all()
        self.withdraw()

    def show(self):
        self.win.grab_set()
        self.deiconify()