# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/projex/xos.py
# Compiled at: 2016-07-03 23:28:12
__doc__ = '\nProvides additional cross platform functionality to the existing\npython os module.\n'
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