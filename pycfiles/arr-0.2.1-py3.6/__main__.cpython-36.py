# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/arr/__main__.py
# Compiled at: 2019-09-30 09:26:27
# Size of source mod 2**32: 837 bytes
import argparse
from arr.star import Star
import pickle, sys, subprocess

def main(args=None):
    if args is None:
        args = sys.argv[1:]
    parser = argparse.ArgumentParser()
    parser.add_argument('target', help='Target to resolve refrences. Must be a name that is resolvable by Simbad.', type=str)
    args = parser.parse_args(args)
    print('Collecting data ... ')
    s = Star(args.target)
    print('Starting shell ... ')
    pickle.dump(s, open('i_obj.arr', 'wb'))
    cmd = ['ipython', '-i', '-c',
     "from arr import Star,Gaia,Tess,Simbad,Reference;import pickle;star : Star = pickle.load(open('i_obj.arr', 'rb'));import os;os.remove('i_obj.arr');import matplotlib.pyplot as pl;pl.ion()"]
    subprocess.call(cmd)


if __name__ == '__main__':
    main()