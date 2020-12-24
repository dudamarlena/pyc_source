# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/lib.linux-i686-2.6/m_lib/m_shutil.py
# Compiled at: 2016-07-25 13:03:41
"""
Shell utilities. Additional to shutil.py (standard library module).
"""
from __future__ import print_function
import os
mkhier_error = 'm_shutil.mkhier_error'

def mkhier(path):
    if os.path.isdir(path):
        return
    if os.path.exists(path):
        raise mkhier_error("`%s' is file" % path)
    list_dirs = path.split(os.sep)
    for i in range(0, len(list_dirs)):
        new_path = os.sep.join(list_dirs[0:i + 1])
        if new_path != '' and not os.path.exists(new_path):
            os.mkdir(new_path)


def mcd(dir):
    os.mkdir(dir)
    os.chdir(dir)


def test():
    mkhier('I.AM/creating/TEST/dir')


if __name__ == '__main__':
    test()