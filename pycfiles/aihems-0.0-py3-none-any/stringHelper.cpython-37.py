# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\aigpy\stringHelper.py
# Compiled at: 2019-10-26 00:11:28
# Size of source mod 2**32: 1185 bytes
__doc__ = '\n@File    :   stringHelper.py\n@Time    :   2019/03/11\n@Author  :   Yaron Huang \n@Version :   1.0\n@Contact :   yaronhuang@qq.com\n@Desc    :   \n'

def isChinese(word, checkPunctuation=False):
    punctuationStr = '，。！？【】（）％＃＠＆１２３４５６７８９０：'
    for ch in word:
        if '一' <= ch <= '\u9fff':
            return True
        if checkPunctuation and punctuationStr.find(ch) != -1:
            return True

    return False


def converPunctuationToEnglish(word):
    table = {ord(f):ord(t) for f, t in zip('，。！？【】（）％＃＠＆１２３４５６７８９０：', ',.!?[]()%#@&1234567890:')}
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
    while num - leng > 0:
        appendStr += ' '
        num -= 1

    if isLeft:
        return string + appendStr
    return appendStr + string