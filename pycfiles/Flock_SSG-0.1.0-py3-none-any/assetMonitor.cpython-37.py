# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\conne\Desktop\Flock_SSG-master\Flock\src\assetMonitor.py
# Compiled at: 2018-12-05 20:23:55
# Size of source mod 2**32: 5032 bytes
from . import settings
from tempfile import mkstemp
from shutil import move
from os import fdopen, remove
import Flock.src.navigator.dirNaviV2 as Navi
import Flock.src.stubber.Stubber2 as dictionary
import string, re, os

def checkAssetStructure(searchFolder):
    stubList = dictionary.getStubList()
    for stub in range(len(stubList)):
        realPath = Navi.findTargetFile(stub, searchFolder)
        if not realPath == dictionary.getPath(stub):
            dictionary.changePath(stub, realPath)


def isValidUrl(url):
    regex = re.compile('^https?://(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\\.)+[A-Z]{2,6}\\.?|localhost|\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}\\.\\d{1,3})(?::\\d+)?(?:/?|[/?]\\S+)$', re.IGNORECASE)
    return url is not None and regex.search(url)


def convertStubsToLinks(searchFolder):
    stubList = dictionary.getStubList()
    for root, dirs, files in os.walk(searchFolder):
        for filename in files:
            if '.md' in filename:
                mdFilePath = os.path.join(root, filename)
                fh, absPath = mkstemp()
                with fdopen(fh, 'w') as (new_file):
                    with open(mdFilePath, 'r+') as (old_file):
                        for line in old_file:
                            if re.search('\\[.*\\]\\(.*\\)', line, flags=0):
                                settings.LOG('Found link\n')
                                tempLine = line
                                tempLine = re.sub('^.*\\[.*\\]', '', tempLine)
                                parsedLine = re.split('[()]', tempLine)
                                tempStub = parsedLine[1]
                                stubInDict = False
                                for subString in parsedLine:
                                    if not isValidUrl(subString):
                                        for stub in stubList:
                                            if subString == stub:
                                                stubInDict = True
                                                tempStub = subString

                                        if stubInDict == False:
                                            settings.LOG('Stub, ' + tempStub + ', not in dictionary')
                                        linkPath = dictionary.getPath(tempStub)
                                        if linkPath == -1:
                                            settings.LOG('Stub, ' + tempStub + ', corresponding path not found in dictionary')
                                            settings.LOG('Substitution will not be carried out, check stubs in files for errors.')
                                        else:
                                            linkPath = re.sub('\\\\', '\\\\\\\\', linkPath)
                                            linkPath = '(' + linkPath + ')'
                                            tempStub = '\\(' + tempStub + '\\)'
                                            line = re.sub(tempStub, linkPath, line)
                                    else:
                                        settings.LOG('\nWARNING: ' + subString + ' identified as a valid URL, no substitution carried out.\n')

                                new_file.write(line)
                            else:
                                new_file.write(line)

                remove(mdFilePath)
                move(absPath, mdFilePath)

    return -1