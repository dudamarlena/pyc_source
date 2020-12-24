# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/pydirduplicatefinder/filters.py
# Compiled at: 2009-08-15 08:24:19
import fnmatch, os

def matchPatterns(path, patterns):
    """Check if the file/directory at the given path match at least one
    of the patterns.
    @path: a path to a file or directory
    @patterns: a list of possible patterns to check
    @return: True id the file/directory name at path match one of the patterns. False otherwise.
    """
    name = os.path.basename(path)
    for p in patterns:
        if fnmatch.fnmatch(name, p):
            return True

    return False