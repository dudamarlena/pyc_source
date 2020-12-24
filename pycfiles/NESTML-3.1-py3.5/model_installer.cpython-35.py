# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pynestml/utils/model_installer.py
# Compiled at: 2020-03-05 05:49:41
# Size of source mod 2**32: 2880 bytes
import os, subprocess, sys

def install_nest(models_path, nest_path):
    """
    This method can be used to install all models located in the ${models} dir into NEST. For the simulator,
    the path to the installation has to be provided (a.k.a. the -Dwith-nest argument of the make command).
    Caution: The nest_path should only point to the install dir, the suffix  /bin/nest-config is automatically attached.
    """
    if not os.path.isdir(models_path):
        print('PyNestML: Models path not a directory (%s)! abort installation...' % models_path)
        return
    if not os.path.isdir(nest_path):
        print('PyNestML: NEST path not a directory (%s)! abort installation...' % nest_path)
        return
    cmake_cmd = [
     'cmake', '-Dwith-nest=' + str(nest_path) + '/bin/nest-config', '.']
    make_all_cmd = ['make', 'all']
    make_install_cmd = ['make', 'install']
    if sys.platform.startswith('win'):
        shell = True
    else:
        shell = False
    try:
        result = subprocess.check_call(cmake_cmd, stderr=subprocess.STDOUT, shell=shell, cwd=str(os.path.join(models_path)))
    except subprocess.CalledProcessError as e:
        print("PyNestML: Something went wrong in 'cmake', see error above!")
        print('abort installation...')
        return

    try:
        subprocess.check_call(make_all_cmd, stderr=subprocess.STDOUT, shell=shell, cwd=str(os.path.join(models_path)))
    except subprocess.CalledProcessError as e:
        print("PyNestML: Something went wrong in 'make all', see error above!")
        print('abort installation...')
        return

    try:
        subprocess.check_call(make_install_cmd, stderr=subprocess.STDOUT, shell=shell, cwd=str(os.path.join(models_path)))
    except subprocess.CalledProcessError as e:
        print("PyNestML: Something went wrong in 'make install', see error above!")
        print('abort installation...')
        return