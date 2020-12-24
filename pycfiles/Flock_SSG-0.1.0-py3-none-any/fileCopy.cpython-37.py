# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\conne\Desktop\Flock_SSG-master\Flock\src\copier\fileCopy.py
# Compiled at: 2018-12-04 23:20:59
# Size of source mod 2**32: 1425 bytes
from .. import settings
import os, shutil

def fileCopy(srcDir, destDir):
    for root, dirs, files in os.walk(srcDir):
        for file in files:
            fullFilePath = os.path.join(root, file)
            if os.path.isfile(fullFilePath):
                settings.LOG(fullFilePath + '  1')
                path = os.path.dirname(fullFilePath)
                path = path.replace('Markdown', '')

    shutil.copytree(srcDir, destDir)
    return True


def deleteMD(folder):
    settings.LOG('Selected directory: ' + folder)
    for root, dirs, files in os.walk(folder):
        for fileName in files:
            if fileName.endswith('.md'):
                try:
                    settings.LOG('Removing markdown file directory')
                    os.remove(os.path.join(root, fileName))
                except:
                    print('An error occured while removing markdown files')
                    return False

    return True