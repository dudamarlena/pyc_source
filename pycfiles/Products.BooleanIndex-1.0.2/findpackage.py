# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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