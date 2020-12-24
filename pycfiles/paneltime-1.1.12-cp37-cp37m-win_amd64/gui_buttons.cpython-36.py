# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: b:\forskning\papers\paneltime\paneltime\paneltime\gui\gui_buttons.py
# Compiled at: 2020-01-08 06:38:30
# Size of source mod 2**32: 2911 bytes
import tkinter as tk, os, traceback
from multiprocessing import pool
from gui import gui_data_objects

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

    def run(self):
        self.win.main_tabs.save_editors()
        if self.buttons['run'][2]:
            return
        try:
            text = self.win.main_tabs.selected_tab_text()
        except:
            return
        else:
            self.run_disable()
            self.pool = pool.ThreadPool(processes=1)
            self.process = self.pool.apply_async((self.exec), (text, self.win.locals, self.win.globals), callback=(self.run_enable))

    def stop(self):
        self.pool.terminate()

    def exec(self, text, glbl, lcl):
        try:
            exec(text, glbl, lcl)
        except Exception as e:
            traceback.print_exc()

    def statistics(self):
        pass

    def open(self):
        a = 0
        filename = tk.filedialog.askopenfilename(initialdir=(self.current_path), title='Open data file', filetypes=(('CSV', '*.csv'),
                                                                                                                    ('text', '*.txt'),
                                                                                                                    ('All files', '*.*')))
        if not filename:
            return
        p, f = os.path.split(filename)
        exe_str = f"load('{filename}')"
        df = eval(exe_str, self.win.locals, self.win.globals)
        self.win.right_tabs.data_tree.data_frames[f] = df
        self.win.right_tabs.data_tree.data_frames_source[f] = exe_str
        self.win.right_tabs.data_tree.add_df_to_tree(df, f)

    def open_sql(self):
        pass

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