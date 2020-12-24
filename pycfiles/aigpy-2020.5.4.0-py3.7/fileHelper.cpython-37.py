# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\aigpy\fileHelper.py
# Compiled at: 2019-10-26 00:11:28
# Size of source mod 2**32: 894 bytes
"""
@File    :   fileHelper.py
@Time    :   2019/03/11
@Author  :   Yaron Huang 
@Version :   1.0
@Contact :   yaronhuang@qq.com
@Desc    :   
"""
import os

def getFileSize(path):
    try:
        if os.path.isfile(path) is False:
            return 0
        return os.path.getsize(path)
    except:
        return 0


def getFileContent(path, isBin=False):
    mode = 'r'
    if isBin:
        mode = 'rb'
    try:
        size = getFileSize(path)
        if size <= 0:
            return ''
        with open(path, mode) as (fd):
            content = fd.read(size)
        return content
    except:
        return ''


def write(path, content, mode):
    try:
        with open(path, mode) as (fd):
            fd.write(content)
        return True
    except Exception as e:
        try:
            return False
        finally:
            e = None
            del e