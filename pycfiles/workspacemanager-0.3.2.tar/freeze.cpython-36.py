# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hayj/Workspace/Python/Organization/WorkspaceManager/workspacemanager/freeze.py
# Compiled at: 2017-09-19 10:41:53
# Size of source mod 2**32: 513 bytes
from workspacemanager.utils import *
import sh

def dispFreeze(theProjectDirectory=None):
    thisLibPackageDirectory, theProjectDirectory, theProjectPackageDirectory, thisLibName = getDirs(theProjectDirectory=theProjectDirectory)
    venvName = theProjectPackageDirectory.split('/')[(-1)] + '-venv'
    print('pip freeze for ' + venvName)
    print(sh.pew('in', venvName, 'pip', 'freeze'))


if __name__ == '__main__':
    dispFreeze()