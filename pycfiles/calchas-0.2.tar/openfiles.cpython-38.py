# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Volumes/USER/gastin/2016/depot_calceph/pythonapi/tests/openfiles.py
# Compiled at: 2017-02-23 12:14:56
# Size of source mod 2**32: 3246 bytes
import os

def prefixsrc(pyarfilename):
    try:
        srcdir = os.environ['srcdir']
        srcdir = srcdir + '/'
        if isinstance(pyarfilename, str):
            pathname = srcdir + pyarfilename
        else:
            pathname = [srcdir + s for s in pyarfilename]
    except:
        pathname = pyarfilename
    else:
        return pathname