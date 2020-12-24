# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/dlblocks/misc.py
# Compiled at: 2018-12-11 12:52:10
import os

def getProjectRoot():
    p = os.getcwd()
    for _ in range(10):
        if os.path.exists(os.path.join(p, '.project_root')):
            return os.path.abspath(p)
        p = os.path.join(p, '..')

    raise ValueError('Project Root not found')


def isnotebook():
    try:
        shell = get_ipython().__class__.__name__
        if shell == 'ZMQInteractiveShell':
            return True
        if shell == 'TerminalInteractiveShell':
            return False
        return False
    except NameError:
        return False


def get_tqdm():
    from tqdm import tqdm_notebook, tqdm
    if isnotebook():
        return tqdm
    else:
        return tqdm