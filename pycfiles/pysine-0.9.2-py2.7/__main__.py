# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pysine/__main__.py
# Compiled at: 2017-08-28 11:27:25
"""
Script to launch pysine from the command line.

Type python -m pysine frequency duration
to generate a sine sound of frequency with duration.
"""
import sys
try:
    from pysine import *
except:
    from . import *

if __name__ == '__main__':
    if len(sys.argv) > 3:
        print 'Wrong number of arguments. '
        print 'Usage: python -m pysine frequency duration'
    else:
        kwargs = dict()
        if len(sys.argv) > 2:
            kwargs['duration'] = float(sys.argv[2])
        if len(sys.argv) > 1:
            kwargs['frequency'] = float(sys.argv[1])
        print 'Calling sine(%s)' % kwargs
        sine(**kwargs)