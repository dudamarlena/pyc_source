# uncompyle6 version 3.7.4
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/pyclearsilver/test.py
# Compiled at: 2005-10-08 14:14:09
"""
usage: %(progname)s [args]
"""
import os, sys, string, time, getopt
from log import *
import odb, odb_sqlite3

def test(name, email):
    print dir()


def usage(progname):
    print __doc__ % vars()


def main(argv, stdout, environ):
    progname = argv[0]
    (optlist, args) = getopt.getopt(argv[1:], '', ['help', 'test', 'debug'])
    testflag = 0
    for (field, val) in optlist:
        if field == '--help':
            usage(progname)
            return
        elif field == '--debug':
            debugfull()
        elif field == '--test':
            testflag = 1

    test('scott', 'hassan@dotfunk.com')


if __name__ == '__main__':
    main(sys.argv, sys.stdout, os.environ)