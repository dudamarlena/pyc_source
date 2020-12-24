# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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