# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\hooks\hook-zope.py
# Compiled at: 2012-10-01 18:12:32
import PyInstaller.hooks.hookutils
from PyInstaller.hooks.hookutils import exec_statement, logger
import os
print 'HOOKING'

def hook(mod):
    logger.info('importing %s' % mod)
    pth = str(mod.__path__[0])
    try:
        import zope.event
        mod.event = zope.event
    except:
        pass

    try:
        import zope.transaction
        mod.transaction = zope.transaction
    except:
        pass

    pth2 = exec_statement('import zope.event; print zope.event.__path__')
    print ('path2', pth2)
    mod.__path__.append(pth2)
    print mod.__path__
    return mod