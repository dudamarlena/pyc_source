# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/phial/utils.py
# Compiled at: 2014-04-22 23:03:09
import glob

def glob_files(files):
    """
    Returns a list of files matching the pattern(s) in ``files``.

    :param files: May be either a string or a list of strings. If a string, the
        pattern will be globbed and all matching files will be returned. If a
        list of strings, all of the patterns will be globbed and all unique
        file paths will be returned.

    :returns: A list of file paths.

    """
    if isinstance(files, basestring):
        result = glob.glob(files)
    else:
        result_set = set()
        for i in files:
            result_set.update(glob.glob(i))

        result = list(result_set)
    return result