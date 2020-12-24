# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hayj/Workspace/Python/Organization/WorkspaceManager/workspacemanager/venv.py
# Compiled at: 2017-09-19 10:41:53
# Size of source mod 2**32: 1272 bytes
from workspacemanager.utils import *
import time, sh

def generateVenv(theProjectDirectory=None):
    argv = argvOptionsToDict()
    if argv is None:
        if theProjectDirectory is None:
            print('Please check the readme for the command usage.')
            exit()
    thisLibPackageDirectory, theProjectDirectory, theProjectPackageDirectory, thisLibName, workspacePath, theProjectName, thePackageName, realPackagePath, realPackageName = getDirs3(theProjectDirectory=theProjectDirectory)
    venvName = thePackageName + '-venv'
    venvsList = sh.pew('ls').split()
    if venvName in venvsList:
        print(venvName + ' already exists.')
    else:
        commandOptions = '-a ' + theProjectDirectory + ' ' + venvName
        if argv is not None:
            if 'p' in argv:
                commandOptions = '-p ' + argv['p'] + ' ' + commandOptions
        commandOptions = 'new -d ' + commandOptions
        print((sh.pew)(*commandOptions.split()))


if __name__ == '__main__':
    pass