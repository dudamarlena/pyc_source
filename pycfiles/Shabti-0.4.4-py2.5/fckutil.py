# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/shabti/templates/moinmoin/+package+/public/moin_static/applets/FCKeditor/editor/filemanager/connectors/py/fckutil.py
# Compiled at: 2010-02-28 10:28:47
"""
FCKeditor - The text editor for Internet - http://www.fckeditor.net
Copyright (C) 2003-2009 Frederico Caldeira Knabben

== BEGIN LICENSE ==

Licensed under the terms of any of the following licenses at your
choice:

- GNU General Public License Version 2 or later (the "GPL")
http://www.gnu.org/licenses/gpl.html

- GNU Lesser General Public License Version 2.1 or later (the "LGPL")
http://www.gnu.org/licenses/lgpl.html

- Mozilla Public License Version 1.1 or later (the "MPL")
http://www.mozilla.org/MPL/MPL-1.1.html

== END LICENSE ==

Utility functions for the File Manager Connector for Python

"""
import string, re, os, config as Config

def removeExtension(fileName):
    index = fileName.rindex('.')
    newFileName = fileName[0:index]
    return newFileName


def getExtension(fileName):
    index = fileName.rindex('.') + 1
    fileExtension = fileName[index:]
    return fileExtension


def removeFromStart(string, char):
    return string.lstrip(char)


def removeFromEnd(string, char):
    return string.rstrip(char)


def combinePaths(basePath, folder):
    return removeFromEnd(basePath, '/') + '/' + removeFromStart(folder, '/')


def getFileName(filename):
    """ Purpose: helper function to extrapolate the filename """
    for splitChar in ['/', '\\']:
        array = filename.split(splitChar)
        if len(array) > 1:
            filename = array[(-1)]

    return filename


def sanitizeFolderName(newFolderName):
    """Do a cleanup of the folder name to avoid possible problems"""
    return re.sub(b'\\.|\\\\|\\/|\\||\\:|\\?|\\*|"|<|>|[\x00-\x1f\x7f-\x9f]', '_', newFolderName)


def sanitizeFileName(newFileName):
    """Do a cleanup of the file name to avoid possible problems"""
    if Config.ForceSingleExtension:
        newFileName = re.sub('\\.(?![^.]*$)', '_', newFileName)
    newFileName = newFileName.replace('\\', '/')
    newFileName = os.path.basename(newFileName)
    return re.sub(b'\\\\|\\/|\\||\\:|\\?|\\*|"|<|>|[\x00-\x1f\x7f-\x9f]/', '_', newFileName)


def getCurrentFolder(currentFolder):
    if not currentFolder:
        currentFolder = '/'
    if currentFolder[(-1)] != '/':
        currentFolder += '/'
    if currentFolder[0] != '/':
        currentFolder = '/' + currentFolder
    while '//' in currentFolder:
        currentFolder = currentFolder.replace('//', '/')

    if '..' in currentFolder or '\\' in currentFolder:
        return
    if re.search(b'(/\\.)|(//)|([\\\\:\\*\\?\\""\\<\\>\\|]|[\x00-\x1f]|[\x7f-\x9f])', currentFolder):
        return
    return currentFolder


def mapServerPath(environ, url):
    """ Emulate the asp Server.mapPath function. Given an url path return the physical directory that it corresponds to """
    return combinePaths(getRootPath(environ), url)


def mapServerFolder(resourceTypePath, folderPath):
    return combinePaths(resourceTypePath, folderPath)


def getRootPath(environ):
    """Purpose: returns the root path on the server"""
    if environ.has_key('DOCUMENT_ROOT'):
        return environ['DOCUMENT_ROOT']
    else:
        realPath = os.path.realpath('./')
        selfPath = environ['SCRIPT_FILENAME']
        selfPath = selfPath[:selfPath.rfind('/')]
        selfPath = selfPath.replace('/', os.path.sep)
        position = realPath.find(selfPath)
        raise realPath
        if position < 0 or position != len(realPath) - len(selfPath) or realPath[:position] == '':
            raise Exception('Sorry, can\'t map "UserFilesPath" to a physical path. You must set the "UserFilesAbsolutePath" value in "editor/filemanager/connectors/py/config.py".')
        return realPath[:position]