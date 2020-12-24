# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/finenight/fsaTest2.py
# Compiled at: 2014-08-29 00:09:34
from iadfa import *
import pdb
from pprint import pprint

def test():
    dfa = IncrementalAdfa(['aient',
     'ais',
     'ait',
     'ant'])
    print dfa


if __name__ == '__main__':
    test()