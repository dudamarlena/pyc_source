# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jqb/projects/boilerplate/boilerplate/utils.py
# Compiled at: 2018-08-06 09:41:19
import os
from os.path import join, dirname, abspath

def create_module_path(thefile, *path):
    root = abspath(join(dirname(abspath(thefile)), *path))
    return lambda *a: join(root, *a)


def _posix_home(*path):
    if 'HOME' not in os.environ:
        return
    return join(os.environ['HOME'], *path)


def _nt_home(*path):
    if 'HOMEDRIVE' not in os.environ:
        return None
    else:
        if 'HOMEPATH' not in os.environ:
            return None
        return join(os.environ['HOMEDRIVE'], os.environ['HOMEPATH'], *path)


_systems = {'posix': _posix_home, 
   'nt': _nt_home}

def userhome_path(*path):
    get_home_path = _systems[os.name]
    return get_home_path(*path)


_systems_paths_sep = {'posix': ':', 
   'nt': ';'}
paths_separator = _systems_paths_sep[os.name]