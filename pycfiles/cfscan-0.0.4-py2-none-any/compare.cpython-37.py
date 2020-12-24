# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/cf/compare.py
# Compiled at: 2019-07-09 05:11:54
# Size of source mod 2**32: 486 bytes
from cf.util import *
from cf.classes import *
import os

def compare(res):
    res = res['result']
    u1 = User(res[0])
    u2 = User(res[1])
    f = open('compare_prof.dat', mode='w')
    f.write('@ ' + u1.handle + ',' + u2.handle + '\n')
    f.write('Rating,' + str(u1.rating) + ',' + str(u2.rating) + '\n')
    f.write('Max Rating,' + str(u1.maxRating) + ',' + str(u2.maxRating) + '\n')
    f.close()
    os.system('termgraph compare_prof.dat --color blue red')
    os.system('rm compare_prof.dat')