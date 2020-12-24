# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Volumes/USER/gastin/2016/depot_calceph/pythonapi/tests/openfiles.py
# Compiled at: 2017-02-23 12:14:56
import os

def prefixsrc(pyarfilename):
    try:
        srcdir = os.environ['srcdir']
        srcdir = srcdir + '/'
        if isinstance(pyarfilename, str):
            pathname = srcdir + pyarfilename
        else:
            pathname = [ srcdir + s for s in pyarfilename ]
    except:
        pathname = pyarfilename

    return pathname