# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.9-intel/egg/cpip/util/CommonPrefix.py
# Compiled at: 2017-06-17 04:30:14
__doc__ = 'Created on 23 Feb 2014\n\n@author: paulross\n'
import os

def lenCommonPrefix(iterable):
    """Returns the length of the common prefix of a list of file names.
    The prefix is limited to directory names."""
    pref = os.path.commonprefix([ os.path.normpath(p) for p in iterable ])
    idx = pref.rfind(os.sep)
    if idx > 0:
        return idx + 1
    return len(pref)