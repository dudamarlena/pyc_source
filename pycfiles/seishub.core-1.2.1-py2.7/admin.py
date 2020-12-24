# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\seishub\core\scripts\admin.py
# Compiled at: 2011-01-03 17:15:11
import sys, os
from seishub.core.daemon import createApplication

def main():
    """
    SeisHub administration script.
    """
    args = sys.argv
    if len(args) == 3:
        if args[1] == 'initenv':
            print 'Initializing new SeisHub environment'
            path = args[2]
            if os.path.isdir(path):
                print 'Error: path %s already exists!' % path
            else:
                createApplication(path, create=True)