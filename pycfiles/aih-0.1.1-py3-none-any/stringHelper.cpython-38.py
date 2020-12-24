# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\aigpy\stringHelper.py
# Compiled at: 2020-02-14 02:12:37
# Size of source mod 2**32: 1140 bytes
__doc__ = '\n@File    :   stringHelper.py\n@Time    :   2019/03/11\n@Author  :   Yaron Huang \n@Version :   1.0\n@Contact :   yaronhuang@qq.com\n@Desc    :   \n'

def isChinese(word, checkPunctuation=False):
    punctuationStr = '，。！？【】（）％＃＠＆１２３４５６７８９０：'
    for ch in word:
        if '一' <= ch <= '\u9fff':
            return True
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