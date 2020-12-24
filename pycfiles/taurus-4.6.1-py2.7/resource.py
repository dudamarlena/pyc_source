# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/taurus/test/resource.py
# Compiled at: 2019-08-19 15:09:30
"""Utility code for working with test resources"""
from __future__ import print_function
import os, sys

def getResourcePath(resmodule, fname=''):
    """
    Returns the absolute path to the directory in which the
    resource module named `resmodule` is implemented.
    If filename is passed, the path to the filename in such directory is
    returned, e.g.:

    getResourcePath('foo.test.res', 'bar.txt') -->
     absolute path to <taurus>/foo/test/res/bar.txt

    It raises ImportError if resmodule does not exist and
    RuntimeError if fname does not exist)

    :param resmodule: (str) name of a resource module
    :param fname: (str) the name of a resource file present in the
                  resmodule directory

    :return: (str) absolute path to the resource file
             (or to the resource directory if fname is not passed)

    """
    __import__(resmodule)
    module = sys.modules[resmodule]
    dirpath = os.path.abspath(os.path.dirname(module.__file__))
    path = os.path.join(dirpath, fname)
    if not os.path.exists(path):
        raise RuntimeError('File "%s" does not exist' % path)
    return path


if __name__ == '__main__':
    print(getResourcePath('taurus.test'))
    print(getResourcePath('taurus.test', 'resource.py'))