# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/stdplus/_writefile.py
# Compiled at: 2018-12-11 10:37:42
# Size of source mod 2**32: 156 bytes


def writefile(filename, contents):
    """Write `contents` to file specified by `filename`"""
    f = open(filename, 'w')
    f.write(contents)
    f.close()