# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: F:\Coding\py\IPython Notebooks\experiment\chunking\LazyEEG\io\save.py
# Compiled at: 2016-10-11 11:48:07
# Size of source mod 2**32: 298 bytes
from ..default import *
import os, pickle

def save_pickle(objname, filename, path='data'):
    if not os.path.exists(path):
        os.mkdir(path)
    if path != '':
        path += '/'
    with open(path + filename, 'wb') as (f):
        pickle.dump(objname, f, pickle.HIGHEST_PROTOCOL)