# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\index\proceed_default2\dir.py
# Compiled at: 2013-09-16 06:11:23
from __future__ import division, absolute_import, print_function, unicode_literals
import os
from ..lib.data_funcs import filter_match, filter_list
from ..reg import reg_object1, set_object
from .models import Dir
from .file import proceed_file

def reg_dir(dirname, options, session, ROOT=None):
    dir_dict = dict(name=dirname)
    DIR = reg_object1(session, Dir, dir_dict, ROOT, style=b'B')
    return DIR


def proceed_dir(dirname, options, session, ROOT=None, HANDLER=None, status=None):
    dirs_filter = options.get(b'dirs_filter')
    files_filter = options.get(b'files_filter')
    for dirname, dirs, files in os.walk(dirname):
        if os.path.isdir(dirname):
            if filter_match(dirname, dirs_filter):
                files_filtered = filter_list(files, files_filter)
                if dirs or files_filtered:
                    DIR = reg_dir(dirname, options, session, ROOT)
                    for basename in files:
                        filename = os.path.join(dirname, basename)
                        if os.path.isfile(filename):
                            if basename in files_filtered:
                                if isinstance(status, dict) and status.get(b'break') == True:
                                    return
                                proceed_file(filename, options, session, DIR, HANDLER)
                            else:
                                set_object(basename, DIR, style=b'D', brief=b'Файл не индексируется!')
                            if isinstance(status, dict):
                                status[b'files'] += 1
                        else:
                            set_object(filename, ROOT, style=b'D', brief=b'Файл не найден!')

                else:
                    set_object(dirname, ROOT, style=b'D', brief=b'Директория без индексных файлов!')
            else:
                set_object(dirname, ROOT, style=b'D', brief=b'Директория не индексируется!')
            if isinstance(status, dict):
                status[b'dirs'] += 1
        else:
            set_object(dirname, ROOT, style=b'D', brief=b'Директория не найдена!')


def proceed_dir_tree(dirname, options, session, ROOT=None, HANDLER=None, status=None):
    DIR = reg_dir(dirname, options, session, ROOT)
    try:
        ldir = os.listdir(dirname)
    except Exception as e:
        set_object(dirname, ROOT, style=b'D', brief=(b'No access: {0}').format(dirname))
        return

    dirs_filter = options.get(b'dirs_filter')
    files_filter = options.get(b'files_filter')
    for basename in sorted(ldir):
        filename = os.path.join(dirname, basename)
        if os.path.isdir(filename):
            if filter_match(basename, dirs_filter):
                proceed_dir_tree(filename, options, session, DIR, HANDLER, status)
            else:
                set_object(filename, DIR, style=b'D', brief=b'Директория не индексируется!')
            if isinstance(status, dict):
                status[b'dirs'] += 1

    for basename in sorted(ldir):
        filename = os.path.join(dirname, basename)
        if os.path.isfile(filename):
            if filter_match(basename, files_filter):
                if isinstance(status, dict) and status.get(b'break') == True:
                    return
                proceed_file(filename, options, session, DIR, HANDLER)
            else:
                set_object(basename, DIR, style=b'D', brief=b'Файл не индексируется!')
            if isinstance(status, dict):
                status[b'files'] += 1

    return DIR