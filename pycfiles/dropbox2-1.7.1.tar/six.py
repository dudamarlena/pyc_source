# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/rick/workspace/dropbox/dropbox/six.py
# Compiled at: 2013-07-08 01:43:34
import sys

def b(str_):
    if sys.version_info >= (3, ):
        str_ = str_.encode('latin1')
    return str_


def u(str_):
    if sys.version_info < (3, ):
        str_ = str_.decode('latin1')
    return str_