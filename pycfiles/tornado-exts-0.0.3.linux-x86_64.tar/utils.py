# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/tornado_extensions/utils.py
# Compiled at: 2013-09-03 05:36:04
import os, fnmatch, re

def check_callable(fun, required=False):
    if required and not fun:
        raise TypeError('callable is required')
    if fun is not None and not callable(fun):
        raise TypeError('callback must be callable')
    return


def file_filter(path='./', patterns=['*']):
    """Filters files in directory with specified patterns
        Example
        -------
        file_filter('./', ["json", "xml"])
    """
    if not isinstance(patterns, list):
        patterns = [
         patterns]
    matching_rule = ('|').join([ pat for pat in patterns ])
    res = []
    for dirpath, dirname, fnames in os.walk(path):
        res = fnmatch.filter(fnames, matching_rule)

    return [ os.path.join(path, f) for f in res ]