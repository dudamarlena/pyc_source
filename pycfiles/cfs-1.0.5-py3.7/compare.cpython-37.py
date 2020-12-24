# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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