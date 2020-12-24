# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sdictviewer/__init__.py
# Compiled at: 2008-05-04 21:40:58
import sdictviewer
from sdictviewer.formats import *
from pyuca import Collator
ucollator = Collator('sdictviewer/allkeys.txt')

def detect_format(file_name):
    fmt_names = [ fmt for fmt in dir(sdictviewer.formats) if not (fmt.startswith('__') or fmt.endswith('__')) ]
    fmts = [ __import__('sdictviewer.formats.' + fmt_name, globals(), locals(), [fmt_name]) for fmt_name in fmt_names ]
    for fmt in fmts:
        if fmt.can_open(file_name):
            return fmt

    return