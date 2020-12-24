# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/misakawa/Doc/flowpython/flowpython/flowpy_switcher/setupfile.py
# Compiled at: 2017-08-29 08:55:56
# Size of source mod 2**32: 3624 bytes
import sys
version = sys.version_info.minor

class windows:
    reps = {
     'py3{}/python3.dll'.format(version),
     'py3{}/python36.dll'.format(version),
     'py3{}/pythonw.exe'.format(version),
     'py3{}/python.exe'.format(version)}


class linux:
    reps = {
     'py3{}/python'.format(version)}


import os, json
from flowpython import __file__ as rootpath
from .utils import makedir_from, moveto, bin_copyto
try:
    user_path = os.environ['HOME']
except KeyError:
    user_path = os.environ['HOMEPATH']

cat = os.path.join

def setup(path, arch, platform):
    flowpy_dir_path = cat(makedir_from(rootpath), f"{platform}-{arch}")
    save_dir_path = cat(makedir_from(rootpath), 'origin_py')
    origin_dir_path = makedir_from(path)
    reps = eval(f"{platform}.reps")
    manager_path = cat(user_path, '.flowpy')

    def enable():
        if not os.path.exists(manager_path):
            pass
        else:
            with open(manager_path, 'r') as (f):
                if json.load(a)['enabled'] == 'true':
                    print('Flowpython has been enabled.')
                    reps.clear()
        if reps:
            for rep in reps:
                oripy_file = cat(origin_dir_path, rep)
                flowpy_file = cat(flowpy_dir_path, rep)
                save_file = cat(save_dir_path, rep)
                moveto(oripy_file, save_file)
                bin_copyto(flowpy_file, oripy_file)
                print('enabled -- {rep}'.format(rep=rep))

            if platform == 'linux':
                os.system('chmod 777 {path}'.format(path=path))
            with open(manager_path, 'w') as (f):
                json.dump({'enabled': 'true'}, f)

    def disable():
        if not os.path.exists(manager_path):
            print('Disable before enabled!!!')
            return
        with open(manager_path, 'r') as (f):
            if json.load(f)['enabled'] == 'true':
                for rep in reps:
                    oripy_file = cat(origin_dir_path, rep)
                    save_file = cat(save_dir_path, rep)
                    moveto(save_file, oripy_file)
                    print('disabled -- {rep}'.format(rep=rep))

                if platform == 'linux':
                    os.system('chmod 777 {path}'.format(path=path))
                with open(manager_path, 'w') as (f):
                    json.dump({'enabled': 'false'}, f)
            else:
                print("Flowpython hasn't been enabled yet!!!")

    def _f_(option):
        ret = enable if option == 'enable' else disable if option == 'disable' else (lambda : print('No option called {option} => do nothing.'.format(option=option)))
        return ret()

    return _f_