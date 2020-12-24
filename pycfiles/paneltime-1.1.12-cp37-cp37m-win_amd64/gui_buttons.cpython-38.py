# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: \\ad.uit.no\uit\data\esi000data\dokumenter\forskning\papers\paneltime\paneltime\paneltime\gui\gui_buttons.py
# Compiled at: 2020-01-14 04:36:46
# Size of source mod 2**32: 3431 bytes
import tkinter as tk
from tkinter import filedialog
import os, traceback
from multiprocessing import pool
from gui import gui_data_objects
from gui import gui_sql

class buttons:

    def __init__(self, win):
        self.win = win
        self.current_path = os.getcwd()
        dirname = os.path.dirname(__file__)
        self.isevaluating = False
        imgs = [('run.png', self.run),
         (
          'stop.png', self.stop),
         (
          'statistics.png', self.statistics),
         (
          'open.png', self.open),
         (
          'open_sql.png', self.open_sql),
         (
          'save.png', self.save),
         (
          'save_as.png', self.save_as)]
        self.buttons = {}
        for i in range(len(imgs)):
            name, action = imgs[i]
            short_name = name.replace('.png', '')
            img = tk.PhotoImage(file=(os.path.join(dirname, 'img', name)), name=short_name)
            img.name
            b = tk.Button((win.button_pane), text='hi', image=img, command=action, highlightthickness=0, bd=0, width=40)
            b.grid(row=0, column=i, sticky=(tk.W))
            self.buttons[short_name] = [img, b, True]
        else:
            imgs = [
             [
              'run_disabled.png', self.buttons['run'][1]],
             [
              'stop_disabled.png', self.buttons['stop'][1]],
             [
              'statistics_disabled.png', self.buttons['statistics'][1]]]
            for name, btn in imgs:
                img = tk.PhotoImage(file=(os.path.join(dirname, 'img', name)), name=(name.replace('.png', '')))
                self.buttons[name.replace('.png', '')] = [img, btn, False]
            else:
                self.gui_sql = None

    def run--- This code section failed: ---

 L.  43         0  LOAD_FAST                'self'
                2  LOAD_ATTR                win
                4  LOAD_ATTR                data
                6  LOAD_METHOD              save
                8  CALL_METHOD_0         0  ''
               10  POP_TOP          

 L.  44        12  LOAD_FAST                'self'
               14  LOAD_ATTR                buttons
               16  LOAD_STR                 'run'
               18  BINARY_SUBSCR    
               20  LOAD_CONST               2
               22  BINARY_SUBSCR    
               24  POP_JUMP_IF_FALSE    30  'to 30'

 L.  45        26  LOAD_CONST               None
               28  RETURN_VALUE     
             30_0  COME_FROM            24  '24'

 L.  46        30  SETUP_FINALLY       168  'to 168'

 L.  47        32  LOAD_FAST                'self'
               34  LOAD_ATTR                win
               36  LOAD_ATTR                main_tabs
               38  LOAD_METHOD              selected_tab_text
               40  CALL_METHOD_0         0  ''
               42  STORE_FAST               'text'

 L.  48        44  LOAD_FAST                'text'
               46  LOAD_METHOD              split
               48  LOAD_STR                 '\n'
               50  CALL_METHOD_1         1  ''
               52  STORE_FAST               's'

 L.  49        54  LOAD_GLOBAL              range
               56  LOAD_GLOBAL              len
               58  LOAD_FAST                's'
               60  CALL_FUNCTION_1       1  ''
               62  CALL_FUNCTION_1       1  ''
               64  GET_ITER         
             66_0  COME_FROM            80  '80'
               66  FOR_ITER             94  'to 94'
               68  STORE_FAST               'i'

 L.  50        70  LOAD_STR                 'import paneltime as pt'
               72  LOAD_FAST                's'
               74  LOAD_FAST                'i'
               76  BINARY_SUBSCR    
               78  COMPARE_OP               in
               80  POP_JUMP_IF_FALSE    66  'to 66'

 L.  51        82  LOAD_FAST                's'
               84  LOAD_METHOD              pop
               86  LOAD_FAST                'i'
               88  CALL_METHOD_1         1  ''
               90  POP_TOP          
               92  JUMP_BACK            66  'to 66'

 L.  52        94  LOAD_STR                 '\n'
               96  LOAD_METHOD              join
               98  LOAD_FAST                's'
              100  CALL_METHOD_1         1  ''
              102  STORE_FAST               'text'

 L.  53       104  LOAD_FAST                'text'
              106  LOAD_METHOD              replace
              108  LOAD_STR                 'pt.execute'
              110  LOAD_STR                 'execute'
              112  CALL_METHOD_2         2  ''
              114  POP_TOP          

 L.  54       116  LOAD_FAST                'text'
              118  LOAD_METHOD              replace
              120  LOAD_STR                 'pt.statistics'
              122  LOAD_STR                 'statistics'
              124  CALL_METHOD_2         2  ''
              126  POP_TOP          

 L.  55       128  LOAD_FAST                'text'
              130  LOAD_METHOD              replace
              132  LOAD_STR                 'pt.load'
              134  LOAD_STR                 'load'
              136  CALL_METHOD_2         2  ''
              138  POP_TOP          

 L.  56       140  LOAD_FAST                'text'
              142  LOAD_METHOD              replace
              144  LOAD_STR                 'pt.load_SQL'
              146  LOAD_STR                 'load_SQL'
              148  CALL_METHOD_2         2  ''
              150  POP_TOP          

 L.  57       152  LOAD_FAST                'text'
              154  LOAD_METHOD              replace
              156  LOAD_STR                 'pt.start()'
              158  LOAD_STR                 ''
              160  CALL_METHOD_2         2  ''
              162  POP_TOP          
              164  POP_BLOCK        
              166  JUMP_FORWARD        182  'to 182'
            168_0  COME_FROM_FINALLY    30  '30'

 L.  58       168  POP_TOP          
              170  POP_TOP          
              172  POP_TOP          

 L.  59       174  POP_EXCEPT       
              176  LOAD_CONST               None
              178  RETURN_VALUE     
              180  END_FINALLY      
            182_0  COME_FROM           166  '166'

 L.  60       182  LOAD_FAST                'self'
              184  LOAD_METHOD              run_disable
              186  CALL_METHOD_0         0  ''
              188  POP_TOP          

 L.  61       190  LOAD_GLOBAL              pool
              192  LOAD_ATTR                ThreadPool
              194  LOAD_CONST               1
              196  LOAD_CONST               ('processes',)
              198  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              200  LOAD_FAST                'self'
              202  STORE_ATTR               pool

 L.  62       204  LOAD_FAST                'self'
              206  LOAD_ATTR                pool
              208  LOAD_ATTR                apply_async
              210  LOAD_FAST                'self'
              212  LOAD_ATTR                exec
              214  LOAD_FAST                'text'
              216  LOAD_FAST                'self'
              218  LOAD_ATTR                win
              220  LOAD_ATTR                globals
              222  LOAD_FAST                'self'
              224  LOAD_ATTR                win
              226  LOAD_ATTR                locals
              228  BUILD_TUPLE_3         3 
              230  LOAD_FAST                'self'
              232  LOAD_ATTR                run_enable
              234  LOAD_CONST               ('callback',)
              236  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              238  LOAD_FAST                'self'
              240  STORE_ATTR               process

Parse error at or near `LOAD_CONST' instruction at offset 176

    def stop(self):
        self.pool.terminate()

    def exec(self, text, glbl, lcl):
        try:
            exec(text, glbl, lcl)
        except Exception as e:
            try:
                traceback.print_exc()
            finally:
                e = None
                del e

    def statistics(self):
        pass

    def open(self):
        a = 0
        filename = filedialog.askopenfilename(initialdir=(self.current_path), title='Open data file', filetypes=(('CSV', '*.csv'),
                                                                                                                 ('text', '*.txt'),
                                                                                                                 ('All files', '*.*')))
        if not filename:
            return
        p, f = os.path.split(filename)
        exe_str = f"load('{filename}')"
        df = eval(exe_str, self.win.locals, self.win.globals)
        self.win.right_tabs.data_tree.data_frames.add(f, df, filename, exe_str)
        self.win.right_tabs.data_tree.add_df_to_tree(df, f)

    def open_sql(self):
        if self.gui_sql is None:
            self.gui_sql = gui_sql.sql_query(self.win, self)
        else:
            self.gui_sql.show()

    def save(self):
        pass

    def save_as(self):
        pass

    def run_disable(self):
        self.new_image('run_disabled')
        self.new_image('stop')

    def run_enable(self, events=None):
        self.new_image('run')
        self.new_image('stop_disabled')

    def new_image(self, img_name):
        img, buttn, enabled = self.buttons[img_name]
        self.buttons[img_name.replace('_disabled', '')][2] = img_name[-9:] == '_disabled'
        buttn.configure(image=img)