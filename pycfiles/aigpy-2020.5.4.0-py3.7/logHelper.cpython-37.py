# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\aigpy\logHelper.py
# Compiled at: 2019-10-26 00:11:28
# Size of source mod 2**32: 670 bytes
"""
@File    :   logHelper.py
@Time    :   2019/02/28
@Author  :   Yaron Huang 
@Version :   1.0
@Contact :   yaronhuang@qq.com
@Desc    :   LOG FILE TOOL
"""
import os, time

def write(path, string):
    try:
        fd = open(path, 'a+')
        fd.write(string + '\n')
        fd.close()
        return True
    except:
        return False


def writeByTime(path, string):
    date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    return write(path, '[' + date + ']  ' + string)


def clear(path):
    try:
        os.remove(path)
    except:
        pass