# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hayj/Workspace/Python/Organization/WorkspaceManager/workspacemanager/setup.py
# Compiled at: 2019-02-08 06:41:58
# Size of source mod 2**32: 5573 bytes
import os, sys, json, getpass
from shutil import *
from os import listdir
from os.path import isfile, join
import datetime
from workspacemanager.utils import *

def getConf(workspacePath):
    conf = dict()
    description = ''
    confPath = workspacePath + '/wm-conf.json'
    if os.path.isfile(confPath):
        with open(confPath) as (confFile):
            try:
                conf = json.load(confFile)
            except ValueError:
                pass

    return conf


def generateSetup(theProjectDirectory=None, userInput=True):
    thisLibPackageDirectory, theProjectDirectory, theProjectPackageDirectory, thisLibName, workspacePath, theProjectName, thePackageName, realPackagePath, realPackageName = getDirs3(theProjectDirectory=theProjectDirectory)
    if theProjectDirectory is not None:
        userInput = False
    if os.path.isfile(theProjectDirectory + '/setup.py'):
        print('Project already setup.')
        exit()
    answer = None
    if userInput:
        answer = input('Do you want to check the directory structure ? Write "N" or press enter: ')
    if not answer == 'N':
        if not os.path.isfile(realPackagePath + '/__init__.py'):
            print('The package of this project must have a __init__.py file.')
            exit()
    conf = getConf(workspacePath)
    if 'author' not in conf or conf['author'] is None:
        author = getpass.getuser()
        authorInput = None
        if userInput:
            authorInput = input('Please write your username or press enter for "' + author + '": ')
        if authorInput is None or len(authorInput) <= 1:
            conf['author'] = author
        else:
            conf['author'] = authorInput
    if 'author_email' not in conf or conf['author_email'] is None:
        conf['author_email'] = None
        if userInput:
            conf['author_email'] = input('Please write your email or press enter: ')
        if conf['author_email'] is None:
            conf['author_email'] = ''
    description = ''
    if userInput:
        description = input('Please write a description or press enter: ')
    templatePath = thisLibPackageDirectory + '/setup-templates'
    allTemplateFiles = [f for f in listdir(templatePath) if isfile(join(templatePath, f))]
    for fileName in allTemplateFiles:
        filePath = templatePath + '/' + fileName
        filePathPaste = theProjectDirectory + '/' + fileName
        print(fileName + ' created.')
        if not os.path.isfile(filePathPaste) and '.pyc' not in filePathPaste:
            copyfile(filePath, filePathPaste)

    now = datetime.datetime.now()
    listSrc = ['<year>', '<copyright holders>']
    listRep = [str(now.year), conf['author']]
    replaceInFile(theProjectDirectory + '/LICENCE.txt', listSrc, listRep)
    print('LICENCE.txt updated.')
    listSrc = [
     '__DESCRIPTION__', '__AUTHOR__', '__AUTHOR_EMAIL__']
    listRep = [description, conf['author'], conf['author_email']]
    replaceInFile(theProjectDirectory + '/setup.py', listSrc, listRep)
    print('setup.py updated.')
    requPath = theProjectDirectory + '/requirements.txt'
    if not os.path.isfile(requPath):
        touch(requPath)
    print('requirements.txt created.')
    toWrite = '__version__ = "0.0.1"'
    initPath = realPackagePath + '/' + '__init__.py'
    if not os.path.isfile(initPath):
        touch(initPath)
    with open(initPath, 'w+') as (f):
        filedata = f.read()
        if filedata is None or len(filedata) == 0 or filedata == '' or filedata == ' ':
            f.write(toWrite)
            print('__version__ added to the __init__.py.')


if __name__ == '__main__':
    generateSetup()