# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hayj/Workspace/Python/Organization/WorkspaceManager/workspacemanager/req.py
# Compiled at: 2018-09-27 16:24:36
# Size of source mod 2**32: 1971 bytes
from workspacemanager.utils import *
import sh

def installReqs(theProjectDirectory=None, venvName=None):
    thisLibPackageDirectory, theProjectDirectory, theProjectPackageDirectory, thisLibName = getDirs(theProjectDirectory=theProjectDirectory)
    if venvName is None:
        venvName = theProjectPackageDirectory.split('/')[(-1)] + '-venv'
    else:
        localDepsPath = theProjectDirectory + '/' + 'local-dependencies.txt'
        reqsPath = theProjectDirectory + '/' + 'requirements.txt'
        reqsPathTmp = getDir(reqsPath) + '/requirements-tmp.txt'
        if isFile(reqsPath):
            print('pip install -r requirements.txt for ' + venvName)
            if isFile(localDepsPath):
                localDeps = fileToStrList(localDepsPath)
                replacementLocalDeps = []
                for current in localDeps:
                    if '/' in current:
                        replacementLocalDeps.append(current.split('/')[(-1)])

                reqs = fileToStrList(reqsPath)
                newReqs = []
                for current in reqs:
                    if current not in replacementLocalDeps:
                        newReqs.append(current)
                    else:
                        print(current + ' will not be installed because a replacement project was found in local dependencies.')

                reqs = newReqs
                strToFile(reqs, reqsPathTmp)
                reqsPath = reqsPathTmp
            print(reqsPath)
            print(sh.pew('in', venvName, 'pip', 'install', '-r', reqsPath))
            removeIfExists(reqsPathTmp)
        else:
            print('No requirements.txt found!')


if __name__ == '__main__':
    installReqs()