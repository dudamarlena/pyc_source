# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\index\proceed_default2\process.py
# Compiled at: 2013-09-26 16:30:56
from __future__ import division, absolute_import, print_function, unicode_literals
import os, logging, xlrd
from ..lib.data_funcs import filter_match, filter_list
from ..reg.result import reg_warning

def proceed(filename, options, session, FILE):
    logging.debug((b'Обработка файла {0}').format(filename))
    basename = os.path.basename(filename)
    root, ext = os.path.splitext(basename)
    ext = ext.lower()
    if hasattr(FILE, b'tree_item'):
        FILE.tree_item.setOk()