# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/cmarzullo/saltscaffold/saltscaffold/formulafolders.py
# Compiled at: 2016-10-15 15:46:35
"""Creates the folder skeleton for a new salt formula"""
import os
from textwrap import dedent

def create_folders(formula_name, current_directory):
    """Creates all the required folders"""
    root_dir = create_path(current_directory, formula_name + '-formula')
    if os.path.exists(root_dir) and os.listdir(root_dir):
        err_msg = ('\n            {directory} already exists and it is not empty.\n\n            Please try a different formula name or root directory.\n\n            ').format(directory=root_dir)
        raise IOError(0, dedent(err_msg))
    else:
        make_folder(root_dir)
    dirnames = (formula_name,
     formula_name + '/files',
     'test/integration/default/serverspec',
     'test/mockup/files')
    for item in dirnames:
        directory = create_path(root_dir, item)
        make_folder(directory, ' +++')


def make_folder(path, prefix=''):
    """Creates the directory and print message"""
    os.makedirs(path)
    if os.path.exists(path) is False:
        err_msg = ('Unable to create root direcotry {path_}. Unknown error!').format(path_=path)
        raise IOError(0, err_msg, '')
    print ('create: {prefix} {path_}').format(prefix=prefix, path_=os.path.abspath(path))


def create_path(current_directory, new_folder_name):
    """Gets the absolute path of the new folder we're creating"""
    current_directory = os.path.abspath(current_directory)
    return os.path.join(current_directory, new_folder_name)