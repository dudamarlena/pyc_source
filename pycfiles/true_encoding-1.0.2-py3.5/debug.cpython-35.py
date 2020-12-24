# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\true_encoding\debug.py
# Compiled at: 2018-01-31 10:02:22
# Size of source mod 2**32: 782 bytes
import re

def debug(res):
    if res.encoding == 'ISO-8859-1' or res.encoding is None:
        if 'charset=gb2312' in res.text or 'charset=GB2312' in res.text:
            return 'gb2312'
        if 'charset=GBK' in res.text or 'charset=gbk' in res.text:
            return 'GBK'
        if 'charset=cp936' in res.text or 'charset=CP936' in res.text:
            return 'cp936'
        if 'charset=utf-8' in res.text or 'charset=UTF-8' in res.text:
            return 'utf-8'
        if 'charset="' in res.text:
            pattern = re.compile('charset="(.*?)"', re.S)
            res.encoding = re.findall(pattern, res.text)[0]
            return res.encoding
        return res.encoding