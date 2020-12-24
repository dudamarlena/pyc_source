# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: b:\forskning\papers\paneltime\paneltime\paneltime\gui\gui.py
# Compiled at: 2020-01-08 06:38:30
# Size of source mod 2**32: 6775 bytes
import tkinter as tk
from tkinter import ttk
from multiprocessing import pool
import sys
from gui import gui_charts
from gui import gui_functions as guif
import os
from gui import gui_buttons
import functions as fu
from gui import gui_right_tabs
from gui import gui_scrolltext
from gui import gui_main_tabs
FONT_SIZE = 10
FONT_WIDTH = FONT_SIZE * 0.35
LINE_HEIGHT = 1.54
GRAPH_IMG_WIDTH = 0.35
GRAPH_IMG_HEIGHT = 0.85

class window(tk.Tk):

    def __init__(self, environment=None):
        tk.Tk.__init__(self)
        self.title('Paneltime')
        self.geometry('%sx%s+%s+%s' % (self.winfo_screenwidth(), self.winfo_screenheight() - 75, -5, 0))
        iconpath = os.path.join(fu.currentdir(), 'paneltime.ico')
        self.iconbitmap(iconpath)
        self.iconpath = iconpath
        self.add_menu()
        self.add_panes()
        self.main_pane.rowconfigure(0, weight=1)
        self.main_pane.columnconfigure(0, weight=100, uniform='fred')
        self.main_pane.columnconfigure(1)
        self.main_pane.columnconfigure(2, weight=20, uniform='fred')
        self.add_main_frames()
        self.add_delimiters()
        self.output = gui_scrolltext.ScrollText(self.frm_left, 2)
        self.right_tabs = gui_right_tabs.right_tab_widget(self)
        self.globals = environment
        self.locals = {'data_frames': self.right_tabs.data_tree.data_frames}
        self.main_tabs = gui_main_tabs.main_tabs(self)
        sys.stdout = stdout_redir(self.output)
        self.protocol('WM_DELETE_WINDOW', self.on_closing)

    def add_panes(self):
        self.rowconfigure(0)
        self.rowconfigure(1, weight=1, uniform='fred')
        self.rowconfigure(2)
        self.columnconfigure(0, weight=1)
        self.button_pane = tk.Frame(self, height=50)
        self.buttons = gui_buttons.buttons(self)
        self.main_pane = tk.Canvas(self, background='pink')
        self.process_bar = tk.Frame(self, height=25)
        self.button_pane.grid(row=0, column=0, sticky=(tk.NW))
        self.process_bar.grid(row=2, column=0, sticky=(tk.S))
        self.main_pane.grid(row=1, column=0, sticky=(tk.NSEW))

    def do_nothing(self, event):
        pass

    def add_delimiters(self):
        self.delimiter_v = tk.Frame((self.frm_left), background='dark grey', height=5, cursor='sb_v_double_arrow')
        self.delimiter_v.grid(row=1, column=0, sticky=(tk.EW))
        self.delimiter_v.bind('<ButtonRelease-1>', self.vertical_resize)
        self.delimiter_h = tk.Frame((self.main_pane), background='dark grey', width=5, cursor='sb_h_double_arrow')
        self.delimiter_h.grid(row=0, column=1, sticky=(tk.NS))
        self.delimiter_h.bind('<ButtonRelease-1>', self.horizontal_resize)

    def add_main_frames(self):
        left_weight = 80
        self.frm_left = tk.Frame((self.main_pane), background='green')
        self.frm_left.rowconfigure(0, weight=left_weight, uniform='fred')
        self.frm_left.rowconfigure(1)
        self.frm_left.rowconfigure(2, weight=(100 - left_weight), uniform='fred')
        self.frm_left.columnconfigure(0, weight=1)
        self.frm_left.grid(row=0, column=0, sticky=(tk.NSEW))
        self.frm_right = tk.Frame((self.main_pane), background='white')
        self.frm_right.rowconfigure(0, weight=1)
        self.frm_right.columnconfigure(0, weight=1)
        self.frm_right.grid(row=0, column=2, sticky=(tk.NSEW))
        self.main_frames_weight = left_weight

    def vertical_resize(self, event):
        self.pack_propagate(0)
        new_y = self.output.winfo_y() + event.y
        y = int(100 * new_y / self.winfo_height())
        self.frm_left.rowconfigure(0, weight=y, uniform='fred')
        self.frm_left.rowconfigure(2, weight=(100 - y), uniform='fred')

    def horizontal_resize(self, event):
        self.pack_propagate(0)
        new_x = self.frm_right.winfo_x() + event.x
        x = int(100 * new_x / self.winfo_width())
        self.main_pane.columnconfigure(0, weight=(max((x, 0))))
        self.main_pane.columnconfigure(2, weight=(max((100 - x, 0))))

    def add_menu(self):
        menubar = tk.Menu(self)
        filemenu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label='File', menu=filemenu)
        openmenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_cascade(label='Open data', menu=openmenu)
        openmenu.add_command(label='Data text file', command=(self.donothing))
        openmenu.add_command(label='Sql connection', command=(self.donothing))
        filemenu.add_command(label='Open project', command=(self.donothing))
        filemenu.add_separator()
        filemenu.add_command(label='Save project', command=(self.donothing))
        filemenu.add_command(label='Save project as', command=(self.donothing))
        filemenu.add_separator()
        filemenu.add_command(label='Settings', command=(self.donothing))
        filemenu.add_separator()
        filemenu.add_command(label='Quit', command=(self.donothing))
        self.settingsmenu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label='Regression', menu=(self.settingsmenu))
        self.settingsmenu.add_command(label='Run Ctrl+R', command=(self.donothing))
        self.settingsmenu.add_command(label='Abort Ctrl+A', command=(self.abort))
        filemenu.add_separator()
        self.settingsmenu.add_command(label='Settings', command=(self.donothing))
        filemenu.add_separator()
        self.settingsmenu.add_command(label='Scatter plots raw', command=(self.show_scatter), state='disabled')
        self.settingsmenu.add_command(label='Scatter plots normalized', command=(self.show_scatter_norm), state='disabled')
        self.config(menu=menubar)

    def donothing(self):
        pass

    def print(self):
        sys.stdout = sys.__stdout__
        print(self.main_tabs.box.get(1.0, tk.END))
        sys.stdout = stdout_redir(self.output)

    def copy(self):
        self.clipboard_clear()
        self.clipboard_append(self.main_tabs.box.get(1.0, tk.END))

    def abort(self):
        if self.btn_abort.cget('relief') == tk.RAISED:
            self.btn_abort.config(relief=(tk.SUNKEN))
        else:
            self.btn_abort.config(relief=(tk.RAISED))

    def update(self, string):
        self.main_tabs.box.insert_all(string)

    def done(self, x):
        sys.stdout = sys.__stdout__
        self.pool.terminate()
        self.destroy()
        self.quit()

    def on_closing(self):
        exit()

    def show_scatter(self):
        if not hasattr(self, 'panel'):
            return
        self.schatter_charts = gui_charts.scatter_charts(self, self.panel, self.panel.input.X, self.panel.input.Y, self.iconpath, 700, 1000)

    def show_scatter_norm(self):
        if not hasattr(self, 'panel') or not hasattr(self, 'll'):
            return
        self.ll.standardize()
        X = self.ll.X_st[self.panel.included[:, :, 0]]
        Y = self.ll.Y_st[self.panel.included[:, :, 0]]
        self.schatter_charts = gui_charts.scatter_charts(self, self.panel, X, Y, self.iconpath, 700, 1000)

    def get(self):
        return self.process.get()

    def save(self):
        print('todo')


class stdout_redir(object):

    def __init__(self, textbox):
        self.textbox = textbox

    def write(self, string):
        self.textbox.insert('end', string)
        self.textbox.see('end')