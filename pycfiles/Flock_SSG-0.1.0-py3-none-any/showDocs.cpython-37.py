# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\conne\Desktop\Flock_SSG-master\Flock\src\docs\showDocs.py
# Compiled at: 2018-12-04 23:20:59
# Size of source mod 2**32: 1891 bytes
from .. import settings
import sys, os, webbrowser
TEXT_TO_WRITE = "The existance of this files tells the program it has been executed before.\nDeleting this file will result in the program performing a first time execution and show the usage documentation.\nYou can also show the usage documentation by calling the program with the '-help' argument.\nThank you for using Flock!"
USAGE_DOC = settings.PREFS_FOLDER + 'docs/Flock-HowTo.html'

def createFile():
    f = open(settings.FIRST_USE_FILE, 'w+')
    f.write(TEXT_TO_WRITE)
    f.close()


def openDocs():
    settings.LOG('Opening usage documentation with the default web-browser\n')
    webbrowser.open(USAGE_DOC, new=0, autoraise=True)


def showDocs(show):
    settings.LOG('Checking if first time use file exists: ')
    isFirstUse = os.path.isfile(settings.FIRST_USE_FILE)
    if not isFirstUse:
        settings.LOG('File does not exist, creating it...\n')
        createFile()
        openDocs()
    else:
        settings.LOG('File exists\n')
    if show == 1:
        openDocs()