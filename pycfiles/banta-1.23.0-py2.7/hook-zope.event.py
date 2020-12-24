# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\hooks\hook-zope.event.py
# Compiled at: 2012-10-01 17:51:20
import PyInstaller.hooks.hookutils
from PyInstaller.hooks.hookutils import exec_statement, logger
import os
print 'HOOKING'

def hook(mod):
    logger.info('importing %s' % mod)
    pth = str(mod.__path__[0])
    pth2 = exec_statement('import zope.event; print zope.event.__path__')
    mod.__path__.append(pth2)
    print ('path', pth)
    print ('path2', pth2)
    if os.path.isdir(pth):
        print pth
    return mod