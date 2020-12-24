# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\winrecon\file_utils.py
# Compiled at: 2019-03-05 14:06:57
# Size of source mod 2**32: 178 bytes
import glob, os

def list_all_files(path):
    print(os.path.join(path, '**'))
    for filename in glob.iglob((os.path.join(path, '**')), recursive=True):
        yield filename