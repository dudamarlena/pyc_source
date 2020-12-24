# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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