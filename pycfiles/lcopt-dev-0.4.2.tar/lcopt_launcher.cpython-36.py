# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: c:\users\pjjoyce\dropbox\00_my_software\lcopt-dev\lcopt\bin\lcopt_launcher.py
# Compiled at: 2018-09-18 05:34:00
# Size of source mod 2**32: 7051 bytes
from tkinter import *
from tkinter import ttk
from tkinter import filedialog, simpledialog
from lcopt.utils import DEFAULT_DB_NAME, FORWAST_PROJECT_NAME, check_for_config, DEFAULT_CONFIG, bw2_project_exists, DEFAULT_PROJECT_STEM
from lcopt.data_store import storage
from lcopt.settings import settings
from lcopt import LcoptModel
import yaml
from brightway2 import *
import os
from pathlib import Path
asset_path = os.path.join(Path(os.path.dirname(os.path.realpath(__file__))).parent, 'assets')
example_ecoinvent_version = '3.3'
example_ecoinvent_system_model = 'cutoff'

def check_databases():
    ecoinvent_present = False
    forwast_present = False
    ei_name = ('Ecoinvent{}_{}_{}'.format)(*example_ecoinvent_version.split('.'), *(example_ecoinvent_system_model,))
    config = check_for_config()
    if config is None:
        config = DEFAULT_CONFIG
        with open(storage.config_file, 'w') as (cfg):
            yaml.dump(config, cfg, default_flow_style=False)
    store_option = storage.project_type
    if store_option == 'single':
        project_name = storage.single_project_name
        if bw2_project_exists(project_name):
            projects.set_current(project_name)
            if ei_name in databases:
                ecoinvent_present = True
            if 'forwast' in databases:
                forwast_present = True
    else:
        project_name = DEFAULT_PROJECT_STEM + ei_name
        ecoinvent_present = bw2_project_exists(project_name)
        forwast_present = bw2_project_exists(FORWAST_PROJECT_NAME)
    return (
     ecoinvent_present, forwast_present)


def main():
    CHECK_ECOINVENT, CHECK_FORWAST = check_databases()
    ECOINVENT_USER = settings.ecoinvent.username not in (None, 'None')
    print('ecoinvent:{}\nforwast:{}\necoinvent user:{}'.format(CHECK_ECOINVENT, CHECK_FORWAST, ECOINVENT_USER))

    def create_model(*args):
        print('Create')
        root.withdraw()
        model_name = simpledialog.askstring('New', 'Enter a name for your model')
        if model_name:
            if ECOINVENT_USER or CHECK_ECOINVENT:
                model = LcoptModel(model_name)
            else:
                model = LcoptModel(model_name, useForwast=True)
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
        if CHECK_ECOINVENT:
            file_path = os.path.join(asset_path, 'ecoinvent_example.lcopt')
            useForwast = False
        else:
            if CHECK_FORWAST:
                file_path = os.path.join(asset_path, 'forwast_example.lcopt')
                useForwast = True
            else:
                if ECOINVENT_USER:
                    print('setting up for ecoinvent')
                    file_path = os.path.join(asset_path, 'ecoinvent_example.lcopt')
                    useForwast = False
                else:
                    print('setting up for forwast')
                    file_path = os.path.join(asset_path, 'forwast_example.lcopt')
                    useForwast = True
            if useForwast:
                print('loading forwast model')
                model = LcoptModel(load=file_path, useForwast=useForwast)
            else:
                model = LcoptModel(load=file_path, ecoinvent_version=example_ecoinvent_version, ecoinvent_system_model=example_ecoinvent_system_model)
        model.launch_interact()
        root.destroy()

    icon = os.path.join(asset_path, 'lcopt_icon.ico')
    root = Tk()
    root.title('LCOPT Launcher')
    root.iconbitmap(icon)
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    initial_width = 425
    initial_height = 175
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
    if CHECK_ECOINVENT:
        ecoinvent_label = 'Yes'
    else:
        ecoinvent_label = 'No'
    if CHECK_FORWAST:
        forwast_label = 'Yes'
    else:
        forwast_label = 'No'
    if ECOINVENT_USER:
        user_label = 'Yes ({})'.format(settings.ecoinvent.username)
    else:
        user_label = 'No'
    ttk.Label(mainframe, text=('  Ecoinvent set up: {}  \n  Forwast set up: {}  \n  Ecoinvent user: {}  '.format(ecoinvent_label, forwast_label, user_label)), foreground='#888', relief='groove').grid(column=0, row=5, columnspan=3, sticky=W)
    if not CHECK_FORWAST:
        if not CHECK_ECOINVENT:
            root.geometry('{}x{}+{}+{}'.format(525, 285, initial_x, initial_y))
            ttk.Label(mainframe, text="WARNING - No background databases have been set up in brightway!\nTo open a model that uses ecoinvent, make sure you've\n entered your username and password in lcopt-settings\nIf you load a model that uses forwast, or load the example model, \nit may take a bit longer as the forwast database is set up", foreground='#8b0000', justify=CENTER).grid(column=1, row=4, columnspan=3)
    for child in mainframe.winfo_children():
        child.grid_configure(padx=5, pady=5)

    root.mainloop()
    print('bye')


if __name__ == '__main__':
    main()