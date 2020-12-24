# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\conne\Desktop\Flock_SSG-master\Flock\src\OScheckLooper.py
# Compiled at: 2018-12-05 20:22:53
# Size of source mod 2**32: 2449 bytes
from . import settings
import platform, os
import Flock.src.stubber.Stubber2 as Stub

def findFile(name, path):
    usrFolder = ''
    try:
        for root, dirs, files in os.walk(path):
            if name in dirs:
                usrFolder = os.path.join(root, name)
                return usrFolder

    except TypeError as typeErr:
        try:
            settings.LOG('Folder  ' + usrFolder + '  does not exist under any path:  ' + path)
            settings.LOG(typeErr)
            settings.LOG('If your directory is stored in an external drive, please move it under your OS drive')
        finally:
            typeErr = None
            del typeErr

    except ValueError as valErr:
        try:
            settings.LOG('Folder  ' + usrFolder + '  does not exist under any path:  ' + path)
            settings.LOG(valErr)
            settings.LOG('If your directory is stored in an external drive, please move it under your OS drive')
        finally:
            valErr = None
            del valErr

    except:
        settings.LOG('Unexpected error!')


def systemCheck(usrDirInput):
    PathInput = ''
    usrPlatform = platform.system()
    if usrPlatform == 'Linux':
        PathInput = '/home'
        fullFolderPath = findFile(usrDirInput, PathInput)
    else:
        if usrPlatform == 'Windows':
            PathInput = 'C:\\'
            fullFolderPath = findFile(usrDirInput, PathInput)
        else:
            if usrPlatform == 'Darwin':
                PathInput = '/Users/'
                fullFolderPath = findFile(usrDirInput, PathInput)
            else:
                print('\nOS not supported\n')
    return fullFolderPath