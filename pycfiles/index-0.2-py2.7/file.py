# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\index\proceed_default2\file.py
# Compiled at: 2013-09-24 05:55:46
from __future__ import division, absolute_import, print_function, unicode_literals
import os
from ..reg import reg_object, set_object
from ..reg.result import reg_debug, reg_warning, reg_exception
from .models import File, FileProcessing
from .process import proceed

def reg_file_processing(filename, options, session, DIR=None, HANDLER=None):
    basename = os.path.basename(filename)
    statinfo = os.stat(filename)
    size = statinfo.st_size
    mtime = statinfo.st_mtime
    FILE = None
    PROCESSING = None
    file_dict = dict(_dir=DIR, name=basename)
    rows = session.query(File).filter_by(**file_dict).all()
    if rows:
        l = len(rows)
        if l > 1:
            reg_warning(DIR, (b'Найдено несколько одинаковых файлов ({0})!').format(l))
        for i in rows:
            FILE = set_object(i, DIR)
            setattr(FILE, b'_records', l)
            processing_dict = dict(_file=FILE, _handler=HANDLER, size=size, mtime=mtime)
            rows2 = session.query(FileProcessing).filter_by(**processing_dict).all()
            if rows2:
                l2 = len(rows2)
                if l2 > 1:
                    reg_warning(FILE, (b'Найдено несколько одинаковых обработок файла ({0})!').format(l2))
                PROCESSING = set_object(rows2[0], FILE)
                setattr(PROCESSING, b'_records', l2)
                break

    if not FILE:
        FILE = reg_object(session, File, file_dict, DIR)
    FILE.size = size
    FILE.mtime = mtime
    if not PROCESSING:
        processing_dict = dict(_file=FILE, _handler=HANDLER, size=size, mtime=mtime)
        PROCESSING = reg_object(session, FileProcessing, processing_dict, FILE)
    return (FILE, PROCESSING)


def proceed_file(filename, options, session, DIR=None, HANDLER=None):
    FILE, PROCESSING = reg_file_processing(filename, options, session, DIR, HANDLER)
    if hasattr(PROCESSING, b'_records'):
        reg_debug(FILE, b'Файл уже обработам, пропускаем!')
        if hasattr(FILE, b'tree_item'):
            FILE.tree_item.set_quiet()
        return
    try:
        proceed(filename, options, session, PROCESSING)
    except Exception as e:
        reg_exception(FILE, e)
        return