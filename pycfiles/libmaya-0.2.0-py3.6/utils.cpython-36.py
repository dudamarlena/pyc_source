# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/maya/exp_runner/utils.py
# Compiled at: 2019-06-13 05:22:46
# Size of source mod 2**32: 615 bytes
import os, shutil
from distutils import dir_util
from collections.abc import Iterable

def clean_dir(dir_path):
    print('cleaning ', dir_path)
    if os.path.exists(dir_path):
        shutil.rmtree(dir_path)
    os.makedirs(dir_path)


def force_copy_tree(src, dst):
    dir_util.copy_tree(src, dst, preserve_symlinks=1)


def copy_as_softlink(src, dst):
    pass


def check_exist(data_name):
    if type(data_name) == str:
        assert os.path.exists(os.path.abspath(data_name))
    else:
        for obj in data_name:
            check_exist(obj)