# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\mempy\myutils.py
# Compiled at: 2016-06-15 22:12:12
# Size of source mod 2**32: 769 bytes
"""
[myutils.py] - Mempire Utilities module

이 모듈은 프로그래밍에 필요한 각종 유틸리티를 구현한 모듈입니다.

"""
__author__ = 'Herokims'
__ver__ = '150114'
__since__ = '2006-10-01'
__update__ = '2015-01-14'
__copyright__ = 'Copyright (c) TreeInsight.org'
__engine__ = 'Python 3.4.1'

def reverseDict(Dict):
    """
    reverseDict(Dictionary Type) -> Dictionary : 
    입력하는 Dictionary 객체의 Key와 Value를 서로 바꾼 Dictionary 객체를 반환.
    """
    return dict((value, key) for key, value in Dict.items())