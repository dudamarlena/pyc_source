# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/hdf5_matlab_reader/tree_printer.py
# Compiled at: 2016-03-22 17:42:02
# Size of source mod 2**32: 280 bytes
from __future__ import division, print_function
import sys, h5py

def disp2(n, o):
    print(n, o)
    print(o.attrs.items())


def tree(f):
    h5_file = h5py.File(f, 'r')
    h5_file.visititems(disp2)


if __name__ == '__main__':
    tree(sys.argv[1])