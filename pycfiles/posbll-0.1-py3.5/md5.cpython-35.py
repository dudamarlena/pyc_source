# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\procode\tools\md5.py
# Compiled at: 2018-11-19 03:00:10
# Size of source mod 2**32: 479 bytes
import hashlib

def genearteMD5(str):
    hl = hashlib.md5()
    hl.update(str.encode(encoding='utf-8'))
    print('MD5加密前为 ：' + str)
    print('MD5加密后为 ：' + hl.hexdigest())
    return hl.hexdigest()


if __name__ == '__main__':
    genearteMD5('123456')