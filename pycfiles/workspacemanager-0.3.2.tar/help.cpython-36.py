# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hayj/Workspace/Python/Organization/WorkspaceManager/workspacemanager/help.py
# Compiled at: 2017-09-19 10:41:53
# Size of source mod 2**32: 698 bytes
import workspacemanager
from .utils import getDirs2
import os.path

def fileToStr(path):
    data = None
    with open(path, 'r') as (myfile):
        data = myfile.read()
    return data


def printHelp():
    print('workspacemanager version: ' + str(workspacemanager.__version__))
    thisLibPackageDirectory, theProjectDirectory, theProjectPackageDirectory, thisLibName, workspacePath, theProjectName, thePackageName = getDirs2()
    readmePath = os.path.abspath(os.path.join(thisLibPackageDirectory, os.pardir)) + '/README.md'
    print(fileToStr(readmePath))


if __name__ == '__main__':
    printHelp()