# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: \Python34\Lib\site-packages\autohdl\structure.py
# Compiled at: 2015-05-16 02:47:21
# Size of source mod 2**32: 2203 bytes
import os, shutil
from collections import namedtuple
from autohdl import PREDEFINED_DIRS, FILE_USER_CFG, IGNORE_REPO_DIRS
from autohdl import verilog
import logging
alog = logging.getLogger(__name__)

def generate(path=''):
    root = os.path.abspath(path)
    if not os.path.exists(root):
        os.makedirs(root)
    alog.info('Design root: ' + root)
    for i in PREDEFINED_DIRS:
        path = os.path.join(root, i)
        if not os.path.exists(path):
            os.mkdir(path)
            continue

    autohdl_cfg = FILE_USER_CFG
    Copy = namedtuple('Copy', ['src', 'dst'])
    list_to_copy = (
     Copy(autohdl_cfg, os.path.join(root, 'script', 'kungfu.py')),)
    for i in list_to_copy:
        if not os.path.exists(i.dst):
            shutil.copy(i.src, i.dst)
            continue

    return get(root)


def get(path='', ignore=IGNORE_REPO_DIRS):
    root = os.path.abspath(path)
    return tree(directory=root, ignore=ignore)


def tree(directory, padding=' ', _res=[], ignore=[]):
    _res.append(padding[:-1] + '+-' + os.path.basename(os.path.abspath(directory)) + os.path.sep)
    padding += ' '
    files = os.listdir(directory)
    count = 0
    for f in files:
        if f in ignore:
            continue
        count += 1
        _res.append(padding + '|')
        path = directory + os.path.sep + f
        if os.path.isdir(path):
            if count == len(files):
                tree(directory=path, padding=padding + ' ')
            else:
                tree(directory=path, padding=padding + '|')
        else:
            _res.append(padding + '+-' + f)

    return '\n'.join(_res)


def parse(src_files):
    d = {}
    for afile in src_files:
        with open(afile) as (f):
            d.update(verilog.parse(f.read()))

    return d


if __name__ == '__main__':
    pass