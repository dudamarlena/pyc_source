# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hayj/Drive/Workspace/Python/Organization/WorkspaceManager/workspacemanager/utils.py
# Compiled at: 2019-02-08 07:25:56
# Size of source mod 2**32: 12717 bytes
import os, errno, sys, subprocess, glob, getpass, sh
from pathlib import Path

def mkdir(path):
    mkdirIfNotExists(path)


def mkdirIfNotExists(path):
    """
        This function make dirs recursively like mkdir -p in bash
    """
    os.makedirs(path, exist_ok=True)


def homeDir():
    return str(Path.home())


def touch(fname, times=None):
    with open(fname, 'a'):
        os.utime(fname, times)


def replaceInFile(path, listSrc, listRep):
    with open(path, 'r') as (f):
        filedata = f.read()
    for i in range(len(listSrc)):
        src = listSrc[i]
        rep = listRep[i]
        filedata = filedata.replace(src, rep)

    with open(path, 'w') as (f):
        f.write(filedata)


def getDirs(theProjectDirectory=None):
    argv = argvOptionsToDict()
    thisLibPackageDirectory = os.path.dirname(os.path.realpath(__file__))
    if theProjectDirectory is None:
        if argv is not None:
            if 'a' in argv:
                theProjectDirectory = argv['a']
    if theProjectDirectory is None:
        theProjectDirectory = os.getcwd()
    if not os.path.isdir(theProjectDirectory):
        print(theProjectDirectory + ' is not a directory.')
        exit()
    theProjectPackageDirectory = theProjectDirectory + '/' + theProjectDirectory.split('/')[(-1)].lower()
    thisLibName = thisLibPackageDirectory.split('/')[(-1)].lower()
    return (
     thisLibPackageDirectory, theProjectDirectory, theProjectPackageDirectory, thisLibName)


def getDirs2(theProjectDirectory=None):
    argv = argvOptionsToDict()
    thisLibPackageDirectory = os.path.dirname(os.path.realpath(__file__))
    if theProjectDirectory is None:
        if argv is not None:
            if 'a' in argv:
                theProjectDirectory = argv['a']
    if theProjectDirectory is None:
        theProjectDirectory = os.getcwd()
    if not os.path.isdir(theProjectDirectory):
        print(theProjectDirectory + ' is not a directory.')
        exit()
    theProjectPackageDirectory = theProjectDirectory + '/' + theProjectDirectory.split('/')[(-1)].lower()
    thisLibName = thisLibPackageDirectory.split('/')[(-1)].lower()
    workspacePath = theProjectDirectory
    while not os.path.isfile(workspacePath + '/wm-conf.json'):
        workspacePath = os.path.abspath(os.path.join(workspacePath, os.pardir))

    theProjectName = theProjectDirectory.split('/')[(-1)]
    thePackageName = theProjectDirectory.split('/')[(-1)].lower()
    return (
     thisLibPackageDirectory,
     theProjectDirectory,
     theProjectPackageDirectory,
     thisLibName,
     workspacePath,
     theProjectName,
     thePackageName)


def getDirs3(theProjectDirectory=None):
    thisLibPackageDirectory, theProjectDirectory, theProjectPackageDirectory, thisLibName, workspacePath, theProjectName, thePackageName = getDirs2(theProjectDirectory=theProjectDirectory)
    firstPackage = None
    currentPackage = None
    correctPackageNameFound = False
    for dirname, dirnames, filenames in os.walk(theProjectDirectory):
        if dirname != theProjectDirectory:
            if dirname != theProjectDirectory + '/.settings':
                currentPackage = dirname
                if firstPackage is None:
                    firstPackage = dirname
            if currentPackage == theProjectPackageDirectory:
                correctPackageNameFound = True
                break

    realPackagePath = None
    if correctPackageNameFound:
        realPackagePath = theProjectPackageDirectory
    else:
        realPackagePath = firstPackage
    realPackageName = realPackagePath.split('/')[(-1)]
    return (
     thisLibPackageDirectory,
     theProjectDirectory,
     theProjectPackageDirectory,
     thisLibName,
     workspacePath,
     theProjectName,
     thePackageName,
     realPackagePath,
     realPackageName)


def getVenvName(theProjectName):
    return theProjectName.lower() + '-venv'


class GlobSortEnum:
    MTIME, NAME, SIZE = list(range(3))


def sortedGlob(regex, caseSensitive=True, sortBy=GlobSortEnum.NAME, reverse=False):

    def insensitiveGlob(pattern):

        def either(c):
            if c.isalpha():
                return '[%s%s]' % (c.lower(), c.upper())
            else:
                return c

        return glob.glob(''.join(map(either, pattern)))

    if caseSensitive:
        paths = glob.glob(regex)
    else:
        paths = insensitiveGlob(regex)
    if sortBy == GlobSortEnum.NAME:
        paths.sort(reverse=reverse)
    else:
        if sortBy == GlobSortEnum.MTIME:
            paths.sort(key=(os.path.getmtime), reverse=reverse)
        else:
            if sortBy == GlobSortEnum.SIZE:
                paths.sort(key=(os.path.getsize), reverse=reverse)
    return paths


def findProject(workspacePath, projectName):
    projectPaths = []
    for root, dirnames, _ in os.walk(workspacePath):
        if projectName in dirnames:
            projectPaths.append(root + '/' + projectName)

    newProjectPaths = []
    for current in projectPaths:
        if '.metadata' not in current:
            newProjectPaths.append(current)

    projectPaths = newProjectPaths
    if projectPaths is None or len(projectPaths) == 0:
        print(projectName + ' not found.')
        return
    else:
        if len(projectPaths) > 1:
            print(projectName + ' conflicts.')
            return
        return projectPaths[0]


def argvOptionsToDict(argv=None):
    """
        This function convert a command in dict key values according to command options.
        If the function return None, it means the argv doesn't have a good format.
        
        :example:
        >>> argvOptionsToDict(argv=["thecommand", "-r", "r", "-a", "a"])
        {'a': 'a', 'r': 'r', 'command': 'thecommand'}
        >>> argvOptionsToDict(argv=["thecommand", "r", "r"]) is None
        True
        >>> argvOptionsToDict(argv=["thecommand"])
        {'command': 'thecommand'}
        >>> argvOptionsToDict(argv=["thecommand", "r"]) is None
        True
        >>> argvOptionsToDict(argv=["thecommand", "--abcd", "/abcd/e"])
        {'abcd': '/abcd/e', 'command': 'thecommand'}
    """
    if argv is None:
        argv = sys.argv
    argvDict = dict()
    if argv is None or len(argv) == 0 or len(argv) % 2 == 0:
        return
    else:
        argvDict['command'] = argv[0]
        for i in range(1, len(argv), 2):
            current = argv[i]
            if len(current) == 2:
                if not current.startswith('-'):
                    return
                argvDict[str(current[1])] = argv[(i + 1)]
            else:
                if len(current) >= 3:
                    if not current.startswith('--'):
                        return
                    argvDict[str(current[2:len(current)])] = argv[(i + 1)]
                else:
                    return

        return argvDict


def getDir(filePath):
    return os.path.dirname(os.path.abspath(filePath))


def getCurrentDir():
    return os.getcwd()


def pathToAbsolute(path):
    if len(path) > 0:
        if path[0] != '/':
            path = getCurrentDir() + '/' + path
    return path


def isFile(filePath):
    filePath = pathToAbsolute(filePath)
    return os.path.isfile(filePath)


def fileToStr(path):
    with open(path, 'r') as (myfile):
        data = myfile.read()
    return data


def fileToStrList(path, strip=True):
    data = fileToStr(path)
    if strip:
        data = data.strip()
    return data.splitlines()


def strToFile(text, path):
    if isinstance(text, list):
        text = '\n'.join(text)
    textFile = open(path, 'w')
    textFile.write(text)
    textFile.close()


def removeIfExists(path):
    try:
        os.remove(path)
    except OSError as e:
        if e.errno != errno.ENOENT:
            raise


def getAllProjects(workspacePath):
    projects = dict()
    for root, subdirs, files in os.walk(workspacePath):
        if '/build/lib' in root:
            pass
        else:
            if 'setup.py' not in files:
                pass
            else:
                allPackagesIn = []
                for currentSubDir in subdirs:
                    currentSubDir = root + '/' + currentSubDir
                    for _, _, currentSubDirFiles in os.walk(currentSubDir):
                        if '__init__.py' in currentSubDirFiles:
                            allPackagesIn.append(currentSubDir)

                if len(allPackagesIn) == 0:
                    pass
                else:
                    projects[root] = allPackagesIn

    keys = list(projects.keys())
    toDelete = set()
    for i in keys:
        for u in keys:
            if u != i and u.startswith(i):
                toDelete.add(u)

    for current in toDelete:
        del projects[current]

    return projects


def getParentDir(path, depth=1):
    for i in range(depth):
        path = os.path.abspath(os.path.join(path, os.pardir))

    return path


def getUser():
    return getpass.getuser()


def strToFile(text, path):
    if isinstance(text, list):
        text = '\n'.join(text)
    textFile = open(path, 'w')
    textFile.write(text)
    textFile.close()


def fileToStr(path, split=False):
    if split:
        return fileToStrList(path)
    else:
        with open(path, 'r') as (myfile):
            data = myfile.read()
        return data


def removeFile(path):
    if not isinstance(path, list):
        path = [
         path]
    for currentPath in path:
        try:
            os.remove(currentPath)
        except OSError:
            pass


def removeIfExistsSecure(path, slashCount=5):
    if path.count('/') >= slashCount:
        removeFile(path)


def getReqs(theProjectDirectory=None):
    thisLibPackageDirectory, theProjectDirectory, theProjectPackageDirectory, thisLibName = getDirs(theProjectDirectory=theProjectDirectory)
    reqsPath = theProjectDirectory + '/' + 'requirements.txt'
    if isFile(reqsPath):
        return reqsPath


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
    print(fileToStrList('/home/hayj/test.txt'))