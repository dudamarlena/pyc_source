# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hayj/Workspace/Python/Organization/WorkspaceManager/workspacemanager/workon.py
# Compiled at: 2017-09-19 10:41:53
# Size of source mod 2**32: 530 bytes
from workspacemanager.utils import *
import sh

def dispWorkon(theProjectDirectory=None):
    thisLibPackageDirectory, theProjectDirectory, theProjectPackageDirectory, thisLibName, workspacePath, theProjectName, thePackageName, realPackagePath, realPackageName = getDirs3(theProjectDirectory=theProjectDirectory)
    venvName = thePackageName + '-venv'
    print('pew workon ' + venvName)


if __name__ == '__main__':
    dispWorkon()