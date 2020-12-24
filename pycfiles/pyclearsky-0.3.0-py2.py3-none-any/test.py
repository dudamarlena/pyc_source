# uncompyle6 version 3.6.7
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/pyclearsilver/test.py
# Compiled at: 2005-10-08 14:14:09
__doc__ = '\nusage: %(progname)s [args]\n'
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