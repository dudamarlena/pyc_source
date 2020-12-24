# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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