# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-intel/egg/cpip/util/CommonPrefix.py
# Compiled at: 2017-06-17 04:30:14
"""Created on 23 Feb 2014

@author: paulross
"""
import os

def lenCommonPrefix(iterable):
    """Returns the length of the common prefix of a list of file names.
    The prefix is limited to directory names."""
    pref = os.path.commonprefix([ os.path.normpath(p) for p in iterable ])
    idx = pref.rfind(os.sep)
    if idx > 0:
        return idx + 1
    return len(pref)