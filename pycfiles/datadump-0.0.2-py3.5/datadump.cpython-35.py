# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/datadump/datadump.py
# Compiled at: 2017-04-25 14:02:29
# Size of source mod 2**32: 956 bytes
import pickle, os
print('Workspace is tmp/ folder by default. Use \n\ndatadump.swd("/path/to/workspace/") \n\nto change this. ')
__WORK_DIR__ = 'tmp/'

def wd():
    global __WORK_DIR__
    return __WORK_DIR__


def pwd():
    print(__WORK_DIR__)


def swd(s):
    global __WORK_DIR__
    if s[(-1)] == '/':
        __WORK_DIR__ = s
    else:
        __WORK_DIR__ = s + '/'


def save(name, *args, **kwargs):
    os.makedirs(__WORK_DIR__, exist_ok=True)
    t = (args, kwargs)
    with open('{}{}.pkl'.format(__WORK_DIR__, name), 'wb') as (f):
        pickle.dump(t, f)
    return t


def load(name):
    with open('{}{}.pkl'.format(__WORK_DIR__, name), 'rb') as (f):
        t = pickle.load(f)
    return t


def ls():
    if os.path.exists(__WORK_DIR__):
        for s in os.listdir(__WORK_DIR__):
            if len(s) >= 4 and s[-4:] == '.pkl':
                print(s[:-4])