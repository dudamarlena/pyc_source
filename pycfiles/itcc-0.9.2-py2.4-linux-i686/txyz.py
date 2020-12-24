# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/itcc/molecule/txyz.py
# Compiled at: 2008-04-20 13:19:45
import numpy

def get_coords(ifile, idxs=None):
    line = ifile.readlines()
    if idxs is None:
        idxs = range(int(line.split()[0]))
    max_idx = max(idxs) + 1
    lines = []
    for i in range(max_idx):
        lines.append(ifile.readline())

    return numpy.array([ [ float(x) for x in lines[i].split()[2:5] ] for i in idxs ])