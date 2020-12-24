# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: \\ad.uit.no\uit\data\esi000data\dokumenter\forskning\papers\paneltime\paneltime\paneltime\gui\gui.py
# Compiled at: 2020-01-27 09:17:31
# Size of source mod 2**32: 10104 bytes
import tkinter as tk, re
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
import tempstore
FONT_SIZE = 10
FONT_WIDTH = FONT_SIZE * 0.35
LINE_HEIGHT = 1.54
GRAPH_IMG_WIDTH = 0.35
GRAPH_IMG_HEIGHT = 0.85

class window(tk.Tk):

    def __init__(self, environment):
        tk.Tk.__init__(self)
        self.title('Paneltime')
        self.globals = environment
        self.geometry('%sx%s+%s+%s' % (self.winfo_screenwidth(), self.winfo_screenheight() - 75, -5, 0))
        iconpath = os.path.join(fu.currentdir(), 'paneltime.ico')
        self.iconbitmap(iconpath)
        self.iconpath = iconpath
        self.add_panes()
        self.main_pane.rowconfigure(0, weight=1)
        self.main_pane.columnconfigure(0, weight=80, uniform='fred')
        self.main_pane.columnconfigure(1)
        self.main_pane.columnconfigure(2, weight=20, uniform='fred')
        self.add_main_frames()
        self.add_delimiters()
        self.output = gui_scrolltext.ScrollText((self.frm_left), format_text=False)
        self.output.grid(row=2, column=0, sticky=(tk.NSEW))
        self.right_tabs = gui_right_tabs.right_tab_widget(self)
        self.locals = {'data_frames': self.right_tabs.data_tree.data_frames}
        self.data = datastore(self)
        self.main_tabs = gui_main_tabs.main_tabs(self)
        sys.stdout = stdout_redir(self.output)
        sys.stderr = stdout_redir(self.output)
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
        self.data.save()
        exit()

    def show_scatter(self):
        if not hasattr(self, 'panel'):
            return
        self.schatter_charts = gui_charts.scatter_charts(self, self.panel, self.panel.input.X, self.panel.input.Y, self.iconpath, 700, 1000)

    def show_scatter_norm(self):
        return hasattr(self, 'panel') and hasattr(self, 'll') or None
        self.ll.standardize()
        X = self.ll.X_st[self.panel.included[:, :, 0]]
        Y = self.ll.Y_st[self.panel.included[:, :, 0]]
        self.schatter_charts = gui_charts.scatter_charts(self, self.panel, X, Y, self.iconpath, 700, 1000)

    def get(self):
        return self.process.get()

    def save(self):
        print('todo')

    def insert_script(self):
        dataset = self.right_tabs.data_tree.get_selected_df()
        script = self.right_tabs.options.script
        script += '\n' + dataset.script
        script = nicify(script)
        txt = self.main_tabs.current_editor(True)
        txt_str = txt.get('1.0', tk.END)
        lines, script_lines = handle_imports(script, txt_str)
        identstr1 = '#Code generated by paneltime:\n'
        identstr2 = '#End code generated by paneltime\n'
        start, end = get_start_end(lines, identstr1, identstr2)
        if start > -1 and end > -1:
            lines = lines[:start + 1] + script_lines + lines[end:]
        else:
            lines.append([identstr1] + script_lines + [identstr2])
        if end == -1:
            end = 0
        elif self.right_tabs.data_tree.script == '':
            txt.replace_all('\n'.join(lines))
            self.data.save()
            return
            script = '\n'.join(lines[start + 3:])
            m = re.search('pt.execute\\(([\\s\\S]*?)\\)', script)
            if m is None:
                txt.replace_all('\n'.join(lines) + '\n\n' + self.right_tabs.data_tree.script)
        else:
            script = script[:m.start()] + self.right_tabs.data_tree.script + script[m.end():]
            txt.replace_all('\n'.join(lines[:start + 3]) + '\n' + script)
        self.data.save()


def handle_imports(script, txt_str):
    imports = [
     'import paneltime as pt']
    new_lines = []
    lines = txt_str.split('\n')
    for i in range(len(lines)):
        s = ' '.join(lines[i].split())
        if 'import' in s:
            if s not in imports:
                imports.append(' '.join(lines[i].split()))
            else:
                new_lines.append(lines[i])
        else:
            script_lines = script.split('\n')
            new_script_lines = []

    for s in script_lines:
        s_stripped = ' '.join(s.split())
        if 'import' in s_stripped:
            if s_stripped not in imports:
                imports.append(s_stripped)
            else:
                new_script_lines.append(s)
        else:
            return (
             imports + new_lines, new_script_lines)


def get_start_end(lines, identstr1, identstr2):
    start = -1
    end = -1
    for i in range(len(lines)):
        if lines[i] == identstr1[:-1] and start == -1:
            start = i
        else:
            if lines[i] == identstr2[:-1] and start > -1:
                end = i
                break
            return (
             start, end)


def nicify(string):
    repl_list = [
     [
      '\n\n', '\n'], ['\r\n', '\n'], ['\n\r', '\n'], ['  ', ' ']]
    for s, r in repl_list:
        while True:
            while True:
                if s in string:
                    string = string.replace(s, r)

            continue

    return string + '\n'


class stdout_redir:

    def __init__(self, textbox):
        self.textbox = textbox

    def write(self, string):
        self.textbox.insert('end', string)
        self.textbox.see('end')


class datastore:

    def __init__(self, window):
        self.dict = tempstore.load_obj(tempstore.fname_window)
        if self.dict is None or type(self.dict) != dict:
            self.dict = dict()
        self.dict_default = dict()
        self.dict_default['sql_str'] = 'SELECT * FROM TABLE <table>'
        self.dict_default['conn_str'] = def_conn_str
        self.win = window

    def get--- This code section failed: ---

 L. 306         0  SETUP_FINALLY        14  'to 14'

 L. 307         2  LOAD_FAST                'self'
                4  LOAD_ATTR                dict
                6  LOAD_FAST                'key'
                8  BINARY_SUBSCR    
               10  POP_BLOCK        
               12  RETURN_VALUE     
             14_0  COME_FROM_FINALLY     0  '0'

 L. 308        14  POP_TOP          
               16  POP_TOP          
               18  POP_TOP          

 L. 309        20  SETUP_FINALLY        42  'to 42'

 L. 310        22  LOAD_FAST                'self'
               24  LOAD_ATTR                dict_default
               26  LOAD_FAST                'key'
               28  BINARY_SUBSCR    
               30  LOAD_FAST                'self'
               32  LOAD_ATTR                dict
               34  LOAD_FAST                'key'
               36  STORE_SUBSCR     
               38  POP_BLOCK        
               40  JUMP_FORWARD         64  'to 64'
             42_0  COME_FROM_FINALLY    20  '20'

 L. 311        42  POP_TOP          
               44  POP_TOP          
               46  POP_TOP          

 L. 312        48  LOAD_CONST               None
               50  LOAD_FAST                'self'
               52  LOAD_ATTR                dict
               54  LOAD_FAST                'key'
               56  STORE_SUBSCR     
               58  POP_EXCEPT       
               60  JUMP_FORWARD         64  'to 64'
               62  END_FINALLY      
             64_0  COME_FROM            60  '60'
             64_1  COME_FROM            40  '40'

 L. 313        64  LOAD_FAST                'self'
               66  LOAD_ATTR                dict
               68  LOAD_FAST                'key'
               70  BINARY_SUBSCR    
               72  ROT_FOUR         
               74  POP_EXCEPT       
               76  RETURN_VALUE     
               78  END_FINALLY      

Parse error at or near `SETUP_FINALLY' instruction at offset 20

    def save(self):
        self.dict['editor_data'] = dict()
        for i in self.win.main_tabs.text_boxes.name_to_textbox:
            self.dict['editor_data'][i] = self.win.main_tabs.text_boxes.name_to_textbox[i].get_all()
        else:
            tempstore.save_obj(tempstore.fname_window, self.dict)


def_conn_str = "conn = pymysql.connect(host='<hostname>', \n\n\t\t\tuser='<username>', \n\t\t\tpasswd='<password>', \n\t\t\tdb='<dbname>')\t"