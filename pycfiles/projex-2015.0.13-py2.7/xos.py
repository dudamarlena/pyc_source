# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/projex/xos.py
# Compiled at: 2016-07-03 23:28:12
"""
Provides additional cross platform functionality to the existing
python os module.
"""
import os, sys

def appdataPath(appname):
    """
    Returns the generic location for storing application data in a cross
    platform way.
    
    :return     <str>
    """
    if sys.platform == 'darwin':
        try:
            from AppKit import NSSearchPathForDirectoriesInDomains
            basepath = NSSearchPathForDirectoriesInDomains(14, 1, True)
            return os.path.join(basepath[0], appname)
        except (ImportError, AttributeError, IndexError):
            basepath = os.path.expanduser('~/Library/Application Support')
            return os.path.join(basepath, appname)

    else:
        if sys.platform == 'win32':
            return os.path.join(os.environ.get('APPDATA'), appname)
        else:
            return os.path.expanduser(os.path.join('~', '.' + appname))