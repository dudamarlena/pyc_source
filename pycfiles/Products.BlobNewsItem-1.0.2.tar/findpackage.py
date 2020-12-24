# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/plone-production-nbf-1/zeocluster/src/Products.BlobNewsItem/Paste-1.7.5.1-py2.6.egg/paste/util/findpackage.py
# Compiled at: 2012-02-27 07:41:58
import sys, os

def find_package(dir):
    """
    Given a directory, finds the equivalent package name.  If it
    is directly in sys.path, returns ''.
    """
    dir = os.path.abspath(dir)
    orig_dir = dir
    path = map(os.path.abspath, sys.path)
    packages = []
    last_dir = None
    while 1:
        if dir in path:
            return ('.').join(packages)
        packages.insert(0, os.path.basename(dir))
        dir = os.path.dirname(dir)
        if last_dir == dir:
            raise ValueError('%s is not under any path found in sys.path' % orig_dir)
        last_dir = dir

    return