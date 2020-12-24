# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\conne\Desktop\Flock_SSG-master\Flock\src\stubber\Stubber2.py
# Compiled at: 2018-12-05 21:34:13
# Size of source mod 2**32: 6128 bytes
from .. import settings
import string, collections, json, os, ast, re
dictonaryOutFile = settings.DICTIONARY_FILE
fileDict = {}
stubList = []

def addToDict(pathTemp):
    global fileDict
    global stubList
    if pathTemp.endswith('.md'):
        pathTemp = pathTemp[:-3] + '.html'
    if pathTemp not in fileDict.keys():
        settings.LOG('Adding new file to dictonary  -  ' + pathTemp)
        pathTempRevrs = pathTemp[::-1]
        stubTemp = pathTempRevrs[pathTempRevrs.index('.') + 1:pathTempRevrs.index('-')]
        stubTemp = stubTemp[::-1]
        fileDict[pathTemp] = stubTemp
        stubList.append(stubTemp)
        fileDictJsonMD = json.dumps(collections.OrderedDict(sorted(fileDict.items())))
        output = open(dictonaryOutFile, 'w')
        output.write(fileDictJsonMD)
        output.close()
        return True
    settings.LOG('File already in dictionary')
    return False


def populateDict(folder):
    filesStubbed = 0
    for root, dirs, files in os.walk(folder):
        for fileName in files:
            if re.search('^\\.', fileName, flags=0):
                continue
            filePath = os.path.join(root, fileName)
            addToDict(filePath)
            filesStubbed += 1

    settings.LOG('\nStubbed ' + str(filesStubbed) + ' files\n')
    return filesStubbed


def getPath(stubTemp):
    pathTemp = ''
    if stubTemp in fileDict.values():
        settings.LOG('Selected stub is in dictonary')
        pathTemp = list(fileDict.keys())[list(fileDict.values()).index(stubTemp)]
        settings.LOG('   Path: ' + pathTemp)
        return pathTemp
    settings.LOG("Stub '" + stubTemp + "' NOT in dictionary.")
    return -1


def getStub(pathTemp):
    stubTemp = ''
    if pathTemp in fileDict.keys():
        settings.LOG('Selected path is in dictonary')
        stubTemp = fileDict[pathTemp]
        settings.LOG('   Stub: ' + stubTemp)
        return stubTemp
    settings.LOG("Path '" + pathTemp + "' NOT in dictionary.")
    return -1


def changePath(stubTemp, pathTemp):
    if stubTemp in fileDict.values():
        del fileDict[list(fileDict.keys())[list(fileDict.values()).index(stubTemp)]]
        fileDict[pathTemp] = stubTemp
        fileDictJson = json.dumps(collections.OrderedDict(sorted(fileDict.items())))
        output = open('Dictionary_output.txt', 'w')
        output.write(fileDictJson)
        output.close()


def getStubList():
    settings.LOG('\n' + str(stubList) + '\n')
    return stubList


def loadDict(nfile):
    global fileDict
    with open(nfile, 'r') as (f):
        s = f.read()
        fileDict = ast.literal_eval(s)
    fileDictJson = json.dumps(collections.OrderedDict(sorted(fileDict.items())))
    output = open('Dictionary_output.txt', 'w')
    output.write(fileDictJson)
    output.close()
    settings.LOG(fileDict)