# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pysine/__main__.py
# Compiled at: 2017-08-28 11:27:25
__doc__ = '\nScript to launch pysine from the command line.\n\nType python -m pysine frequency duration\nto generate a sine sound of frequency with duration.\n'
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