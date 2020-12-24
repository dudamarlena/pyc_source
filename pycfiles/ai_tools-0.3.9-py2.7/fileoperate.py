# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ai_tools/fileoperate.py
# Compiled at: 2018-09-17 01:29:31
import os, shutil

def rmdirfile(dirname):
    files = os.listdir(dirname)
    for file in files:
        if os.path.getsize(file) < minSize * 1000:
            os.remove(file)
            print file + ' deleted'


def rmdir(dirname):
    if os.path.isdir(dirname):
        shutil.rmtree(dirname)