# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/bung/.virtualenvs/whatlangid/lib/python3.5/site-packages/cppjieba_py/posseg.py
# Compiled at: 2018-08-18 04:51:59
# Size of source mod 2**32: 178 bytes
import libcppjieba

def cut(sentence, HMM=False):
    it = libcppjieba.tag(sentence)
    return iter(it)


def lcut(sentence, HMM=False):
    return libcppjieba.tag(sentence)