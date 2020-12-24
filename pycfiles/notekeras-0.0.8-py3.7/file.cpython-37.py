# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/notekeras/utils/file.py
# Compiled at: 2020-03-29 09:28:39
# Size of source mod 2**32: 288 bytes
import os

def read_lines(file_name):
    """loads class name from a file"""
    classes_path = os.path.expanduser(file_name)
    with open(classes_path, encoding='utf8') as (f):
        class_names = f.readlines()
    class_names = [c.strip() for c in class_names]
    return class_names