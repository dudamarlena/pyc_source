# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sdktool/test.py
# Compiled at: 2020-04-03 04:51:46
import random, pprint, os, fcntl, time
from util.Config import *
from util.utils import BasicConfig
MAX = 10000000
FNAME = 'test0324del.txt'

def genfile():
    fp = open(FNAME, 'w+')
    for i in range(MAX):
        fp.write(str(random.randint(0, MAX)) + '\n')

    fp.close()


def cc():
    print BasicConfig.calhash('test0312small.txt')


cc()