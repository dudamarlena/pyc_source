# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/philippebordron/git/work/sgs-utils/src/sgs_utils/plop.py
# Compiled at: 2016-03-17 14:43:17
import sys, os
PKG = 'plop'

def echo(caller):
    print ('I am module {} called by {}').format(PKG, caller)


def main(argv, prog=os.path.basename(sys.argv[0])):
    echo(prog)


if __name__ == '__main__':
    main(sys.argv[1:])