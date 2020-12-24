# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/ltpackagetemplate/exector.py
# Compiled at: 2019-03-27 10:11:20
# Size of source mod 2**32: 1004 bytes
import os, sys, getopt
from .utils import *

def main(argv):
    global out_put
    try:
        opts, args = getopt.getopt(argv, 's:h', ['string', 'help'])
    except getopt.GetoptError:
        warning(__doc__)
        sys.exit(2)

    for opt, arg in opts:
        if opt in {'--string', '-s'}:
            out_put = arg

    __do_exec()


out_put = 'hello world'

def __do_exec():
    PrintWithColor.black('').fore_green().style_underline().apply((f"{out_put}"), end='\n\n')


if __name__ == '__main__':
    main(sys.argv[1:])