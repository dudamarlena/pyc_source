# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\biosignalsnotebooks\notebook_files\__update_content__.py
# Compiled at: 2020-03-23 15:40:39
# Size of source mod 2**32: 1893 bytes
"""
    Private module uniquely dedicated to clone the last version of bsnb_files, from the
    biosignalsnotebooks original folder.

"""
import os, shutil

def run_update():
    current_dir = os.path.abspath(__file__).split(os.path.basename(__file__))[0].replace('\\', '/')
    aux_dir = current_dir + 'osf_files/'
    for folder in ('images', 'signal_samples', 'styles'):
        if os.path.isdir(aux_dir + folder):
            shutil.rmtree(aux_dir + folder)
        src = '../../../biosignalsnotebooks_notebooks/' + folder
        if os.path.isdir(src):
            shutil.copytree(src, aux_dir + folder)
        else:
            raise RuntimeError('The current module has a private state. It should only be used by the package developers!')

    if not os.path.exists(aux_dir + 'aux_folders'):
        os.makedirs(aux_dir + 'aux_folders')
    src = '../../../biosignalsnotebooks_notebooks/Categories'
    categories = os.listdir(src)
    for category in ('MainFiles', ):
        possible_src = src + '/' + category + '/aux_files'
        if os.path.isdir(possible_src):
            dst = aux_dir + 'aux_folders/' + category + '/aux_files'
            if os.path.isdir(dst):
                shutil.rmtree(dst)
            shutil.copytree(possible_src, dst)


run_update()