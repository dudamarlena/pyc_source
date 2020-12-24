# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hayj/Workspace/Python/Organization/WorkspaceManager/workspacemanager/condaadd.py
# Compiled at: 2019-02-08 07:27:59
# Size of source mod 2**32: 1492 bytes
"""
        This script add all project path to conda-venv

        https://stackoverflow.com/questions/37006114/anaconda-permanently-include-external-packages-like-in-pythonpath
"""
import os, sh
from workspacemanager.utils import *
from pathlib import Path
import sys

def homeDir():
    return str(Path.home())


def generatePythonpath():
    venvName = 'conda-venv'
    workspacePath = homeDir() + '/Workspace'
    sitePackagePath = sortedGlob(homeDir() + '/lib/anaconda*/envs/conda-venv/lib/python3.*/site-packages')[0]
    projects = getAllProjects(workspacePath)
    scriptDir = homeDir() + '/tmp'
    mkdir(scriptDir)
    condaLibPath = '/home/hayj/lib/anaconda3/bin'
    scriptPath = scriptDir + '/tmp-script-for-conda-add.sh'
    for projectPath in projects:
        scriptContent = ''
        scriptContent += 'source ' + condaLibPath + '/activate conda-venv' + '\n'
        scriptContent += condaLibPath + '/conda develop ' + projectPath + '\n'
        strToFile(scriptContent, scriptPath)
        print(sh.bash(scriptPath))
        removeIfExists(scriptPath)


if __name__ == '__main__':
    generatePythonpath()