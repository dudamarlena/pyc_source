# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hayj/Workspace/Python/Organization/WorkspaceManager/workspacemanager/deps.py
# Compiled at: 2017-09-19 10:41:53
# Size of source mod 2**32: 2794 bytes
import os, sys
from workspacemanager.utils import *
from workspacemanager.test.utils import fileToStr
import sh

def installDeps(theProjectDirectory=None, theProjectVenvName=None, alreadyLocalInstalled=None, indent=0):
    argv = argvOptionsToDict()
    if argv is None:
        print('Please check the readme for the command usage.')
        exit()
    indentText = '\t' * indent
    thisLibPackageDirectory, theProjectDirectory, theProjectPackageDirectory, thisLibName, workspacePath, theProjectName, thePackageName = getDirs2(theProjectDirectory=theProjectDirectory)
    if theProjectVenvName is None:
        theProjectVenvName = thePackageName + '-venv'
    filePath = theProjectDirectory + '/local-dependencies.txt'
    if 'r' in argv:
        filePath = theProjectDirectory + '/' + argv['r']
    if alreadyLocalInstalled is None:
        alreadyLocalInstalled = [
         theProjectName]
    if os.path.isfile(filePath):
        with open(filePath, 'r') as (f):
            for line in f:
                line = line.strip()
                if '/' in line:
                    line = line.split('/')[0]
                if len(line) > 0 and line not in alreadyLocalInstalled:
                    alreadyLocalInstalled.append(line)
                    currentDepPath = findProject(workspacePath, line)
                    if os.path.isdir(currentDepPath):
                        print(indentText + 'Installing ' + line + '...')
                        sh.cd(currentDepPath)
                        sh.pew('in', theProjectVenvName, 'python', 'setup.py', 'install')
                        sh.pew('in', theProjectVenvName, 'pip', 'install', '-r', 'requirements.txt')
                        installDeps(theProjectDirectory=currentDepPath, theProjectVenvName=theProjectVenvName, alreadyLocalInstalled=alreadyLocalInstalled, indent=(indent + 1))
                    else:
                        print(line + " doesn't exist.")


if __name__ == '__main__':
    installDeps()