# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/dirwalker/dirwalker.py
# Compiled at: 2015-07-23 12:16:18
import os
from os.path import join, getsize
from os import path

def file_lister(source, ignore_hidden=True, file_exceptions=[], dir_exceptions=[]):
    orig_dir = os.getcwd()
    os.chdir(source)
    exception_list = []
    for exception in dir_exceptions:
        exception_list.append(user_parse(exception))

    ignore_files = []
    for item in file_exceptions:
        ignore_files.append(user_parse(item))

    file_list = []
    for root, dirs, files in os.walk(source, topdown=True):
        dirs[:] = [ d for d in dirs if join(root, d) not in exception_list ]
        if ignore_hidden == True:
            dirs[:] = [ d for d in dirs if not d.startswith('.') ]
        for f in files:
            if f.startswith('.'):
                pass
            elif os.path.join(root, f) in ignore_files:
                pass
            else:
                file_list.append(join(root, f))

    os.chdir(orig_dir)
    return file_list


def user_parse(file_path):
    item_path = None
    item_base = None
    item_path = os.path.expanduser(os.path.dirname(file_path))
    item_base = os.path.basename(file_path)
    return os.path.join(item_path, item_base)