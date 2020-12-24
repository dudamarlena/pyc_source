# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-intel/egg/labmanager/util.py
# Compiled at: 2014-02-26 03:46:25
__author__ = [
 'markshao']
import os
try:
    from cPickle import load, dump
except ImportError:
    from pickle import load, dump

def write_json_fd(dist, fpath):
    if os.path.exists(fpath):
        os.remove(fpath)
    f = open(fpath, 'wb')
    dump(dist, f)
    f.close()


def read_dict_fd(fpath):
    f = open(fpath, 'rb')
    obj = load(f)
    f.close()
    return obj