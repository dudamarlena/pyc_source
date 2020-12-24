# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/comdutils/file_utils.py
# Compiled at: 2019-03-19 04:16:32
# Size of source mod 2**32: 144 bytes
from os import walk

def get_filenames(path):
    f = []
    for dirpath, dirnames, filenames in walk(path):
        f.extend(filenames)
        break

    return f