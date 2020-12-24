# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/pbr/extra_files.py
# Compiled at: 2017-12-04 07:19:32
from distutils import errors
import os
_extra_files = []

def get_extra_files():
    global _extra_files
    return _extra_files


def set_extra_files(extra_files):
    for filename in extra_files:
        if not os.path.exists(filename):
            raise errors.DistutilsFileError('%s from the extra_files option in setup.cfg does not exist' % filename)

    _extra_files[:] = extra_files[:]