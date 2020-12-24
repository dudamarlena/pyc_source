# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\aigpy\logHelper.py
# Compiled at: 2019-10-26 00:11:28
# Size of source mod 2**32: 670 bytes
__doc__ = '\n@File    :   logHelper.py\n@Time    :   2019/02/28\n@Author  :   Yaron Huang \n@Version :   1.0\n@Contact :   yaronhuang@qq.com\n@Desc    :   LOG FILE TOOL\n'
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