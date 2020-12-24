# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\aigpy\stringHelper.py
# Compiled at: 2020-02-14 02:12:37
# Size of source mod 2**32: 1140 bytes
"""
@File    :   stringHelper.py
@Time    :   2019/03/11
@Author  :   Yaron Huang 
@Version :   1.0
@Contact :   yaronhuang@qq.com
@Desc    :   
"""

def isChinese(word, checkPunctuation=False):
    punctuationStr = '，。！？【】（）％＃＠＆１２３４５６７８９０：'
    for ch in word:
        if '一' <= ch <= '\u9fff':
            return True
        if checkPunctuation and punctuationStr.find(ch) != -1:
            return True
        return False


def converPunctuationToEnglish(word):
    table = {ord(t):ord(f) for f, t in zip('，。！？【】（）％＃＠＆１２３４５６７８９０：', ',.!?[]()%#@&1234567890:')}
    ret = word.translate(table)
    return ret


def align(string, num, isLeft=True):
    leng = 0
    for c in string:
        leng += 1
        if isChinese(c, True):
            leng += 1
        if leng >= num:
            return string
            appendStr = ''
            if num - leng > 0:
                appendStr += ' '
                num -= 1
        else:
            if isLeft:
                return string + appendStr
            return appendStr + string