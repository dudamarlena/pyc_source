# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: c:\users\pjjoyce\dropbox\04. redmud ip lca project\04. modelling\lcopt\lcopt\bin\lcopt_bw2_setup.py
# Compiled at: 2017-08-18 11:04:52
# Size of source mod 2**32: 189 bytes
from sys import argv
from lcopt.utils import lcopt_bw2_setup

def main():
    ecospold_path = argv[1]
    lcopt_bw2_setup(ecospold_path)


if __name__ == '__main__':
    main()