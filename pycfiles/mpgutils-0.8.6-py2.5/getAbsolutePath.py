# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/mpgutils/getAbsolutePath.py
# Compiled at: 2008-12-08 13:15:31
"""usage: %prog <path>

Creates an absolute path from a relative path.
"""
from __future__ import division
import optparse, sys
from os.path import abspath

def main(argv=None):
    if argv is None:
        argv = sys.argv
    parser = optparse.OptionParser(usage=__doc__)
    (dctOptions, lstArgs) = parser.parse_args(argv)
    if len(lstArgs) != 2:
        print >> sys.stderr, 'ERROR: Must have exactly 1 argument.\n'
        parser.print_help()
        return 1
    strPath = lstArgs[1]
    strAbsPath = abspath(strPath)
    print strAbsPath
    return


if __name__ == '__main__':
    sys.exit(main())