# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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