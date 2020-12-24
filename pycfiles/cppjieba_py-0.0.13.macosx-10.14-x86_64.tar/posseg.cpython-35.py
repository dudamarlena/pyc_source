# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bung/.virtualenvs/whatlangid/lib/python3.5/site-packages/cppjieba_py/posseg.py
# Compiled at: 2018-08-18 04:51:59
# Size of source mod 2**32: 178 bytes
import libcppjieba

def cut(sentence, HMM=False):
    it = libcppjieba.tag(sentence)
    return iter(it)


def lcut(sentence, HMM=False):
    return libcppjieba.tag(sentence)