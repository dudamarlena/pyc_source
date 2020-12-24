# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dexter/git/tensorboardX/tensorboardX/beholder/file_system_tools.py
# Compiled at: 2019-08-01 11:57:19
# Size of source mod 2**32: 1161 bytes
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import pickle

def write_file(contents, path, mode='wb'):
    with open(path, mode) as (new_file):
        new_file.write(contents)


def write_pickle(obj, path):
    with open(path, 'wb') as (new_file):
        pickle.dump(obj, new_file)


def read_pickle(path, default=None):
    with open(path, 'rb') as (pickle_file):
        result = pickle.load(pickle_file)
    return result