# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\mempy\mysys.py
# Compiled at: 2016-06-15 21:30:42
# Size of source mod 2**32: 785 bytes
"""
[mysys.py] - Mempire System Management module

이 모듈은 시스템을 관리하기 위해 필요한 유틸리티 기능을 구현한 모듈입니다.

"""
__author__ = 'Herokims'
__ver__ = '150114'
__since__ = '2006-10-01'
__update__ = '2006-10-01'
__copyright__ = 'Copyright (c) TreeInsight.org'
__engine__ = 'Python 3.4.1'
import os

def getCurdir():
    return os.getcwd()


def isExist(pathName):
    return os.path.exists(pathName)


def makeDir(pathName):
    try:
        os.makedirs(pathName)
        return True
    except:
        return False