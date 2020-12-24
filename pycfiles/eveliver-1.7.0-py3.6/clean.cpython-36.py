# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/eveliver/clean.py
# Compiled at: 2020-03-19 03:31:58
# Size of source mod 2**32: 222 bytes
import os, shutil

def clean():
    os.chdir('r')
    for d in os.listdir():
        if not os.path.exists(os.path.join(d, 'output', 'f.json')):
            shutil.rmtree(d)


if __name__ == '__main__':
    clean()