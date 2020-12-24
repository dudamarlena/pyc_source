# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: c:\users\pjjoyce\dropbox\04. redmud ip lca project\04. modelling\lcopt\lcopt\bin\lcopt_launcher.py
# Compiled at: 2017-08-21 11:34:17
# Size of source mod 2**32: 3724 bytes
from tkinter import *
from tkinter import ttk
from tkinter import filedialog, simpledialog
from lcopt.utils import DEFAULT_DB_NAME, FORWAST_DB_NAME
from lcopt import LcoptModel
from brightway2 import *
import os
from pathlib import Path

def check_databases():
    return (
     DEFAULT_DB_NAME in projects, FORWAST_DB_NAME in projects)


def main():
    CHECK_ECOINVENT, CHECK_FORWAST = check_databases()

    def create_model(*args):
        print('Create')
        root.withdraw()
        model_name = simpledialog.askstring('New', 'Enter a name for your model')
        if model_name:
            model = LcoptModel(model_name)
            model.launch_interact()
        root.destroy()

    def load_model(*args):
        print('Load')
        root.withdraw()
        titleString = 'Choose a model to open'
        filetypesList = [('Lcopt model files', '.lcopt')]
        file_path = filedialog.askopenfilename(title=titleString, filetypes=filetypesList)
        print(file_path)
        if file_path:
            model = LcoptModel(load=file_path)
            model.launch_interact()
        root.destroy()

    def load_example(*args):
        print('Load example')
        root.withdraw()
        asset_path = os.path.join(Path(os.path.dirname(os.path.realpath(__file__))).parent, 'assets')
        if CHECK_ECOINVENT:
            file_path = os.path.join(asset_path, 'ecoinvent_example.lcopt')
        else:
            if CHECK_FORWAST:
                file_path = os.path.join(asset_path, 'forwast_example.lcopt')
            else:
                root.destroy()
                return
        model = LcoptModel(load=file_path)
        model.launch_interact()
        root.destroy()

    root = Tk()
    root.title('LCOPT Launcher')
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    initial_width = 425
    initial_height = 125
    initial_x = int(screen_width / 2 - initial_width / 2)
    initial_y = int(screen_height / 2 - initial_height / 2)
    root.geometry('{}x{}+{}+{}'.format(initial_width, initial_height, initial_x, initial_y))
    mainframe = ttk.Frame(root, padding='20 20 20 20')
    mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
    mainframe.columnconfigure(0, weight=1)
    mainframe.rowconfigure(0, weight=1)
    ttk.Label(mainframe, text='Welcome to the LCOPT Launcher').grid(column=1, row=1, columnspan=3)
    ttk.Button(mainframe, text='Create Model', command=create_model).grid(column=1, row=2, sticky=W)
    ttk.Button(mainframe, text='Open Model', command=load_model).grid(column=2, row=2, sticky=E)
    btn_example = ttk.Button(mainframe, text='Open Example Model', command=load_example)
    btn_example.grid(column=3, row=2, sticky=E)
    if not CHECK_FORWAST:
        if not CHECK_ECOINVENT:
            root.geometry('{}x{}+{}+{}'.format(initial_width, 175, initial_x, initial_y))
            ttk.Label(mainframe, text='WARNING - No databases have been set up in brightway!\nUse lcopt-bw2-setup or lcopt-bw2-setup-forwast\n(see Installation section of the docs)', foreground='#8b0000', justify=CENTER).grid(column=1, row=4, columnspan=3)
            btn_example.state(['disabled'])
    for child in mainframe.winfo_children():
        child.grid_configure(padx=5, pady=5)

    root.mainloop()
    print('bye')


if __name__ == '__main__':
    main()