# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/shabti/templates/moinmoin/+package+/public/moin_static/applets/FCKeditor/editor/filemanager/connectors/py/fckcommands.py
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

Connector for Python (CGI and WSGI).

"""
import os
try:
    import msvcrt
    msvcrt.setmode(0, os.O_BINARY)
    msvcrt.setmode(1, os.O_BINARY)
except ImportError:
    pass

from fckutil import *
from fckoutput import *
import config as Config

class GetFoldersCommandMixin(object):

    def getFolders(self, resourceType, currentFolder):
        """
                Purpose: command to recieve a list of folders
                """
        serverPath = mapServerFolder(self.userFilesFolder, currentFolder)
        s = '<Folders>'
        for someObject in os.listdir(serverPath):
            someObjectPath = mapServerFolder(serverPath, someObject)
            if os.path.isdir(someObjectPath):
                s += '<Folder name="%s" />' % convertToXmlAttribute(someObject)

        s += '</Folders>'
        return s


class GetFoldersAndFilesCommandMixin(object):

    def getFoldersAndFiles(self, resourceType, currentFolder):
        """
                Purpose: command to recieve a list of folders and files
                """
        serverPath = mapServerFolder(self.userFilesFolder, currentFolder)
        folders = '<Folders>'
        files = '<Files>'
        for someObject in os.listdir(serverPath):
            someObjectPath = mapServerFolder(serverPath, someObject)
            if os.path.isdir(someObjectPath):
                folders += '<Folder name="%s" />' % convertToXmlAttribute(someObject)
            elif os.path.isfile(someObjectPath):
                size = os.path.getsize(someObjectPath)
                if size > 0:
                    size = round(size / 1024)
                    if size < 1:
                        size = 1
                files += '<File name="%s" size="%d" />' % (
                 convertToXmlAttribute(someObject),
                 size)

        folders += '</Folders>'
        files += '</Files>'
        return folders + files


class CreateFolderCommandMixin(object):

    def createFolder(self, resourceType, currentFolder):
        """
                Purpose: command to create a new folder
                """
        errorNo = 0
        errorMsg = ''
        if self.request.has_key('NewFolderName'):
            newFolder = self.request.get('NewFolderName', None)
            newFolder = sanitizeFolderName(newFolder)
            try:
                newFolderPath = mapServerFolder(self.userFilesFolder, combinePaths(currentFolder, newFolder))
                self.createServerFolder(newFolderPath)
            except Exception, e:
                errorMsg = str(e).decode('iso-8859-1').encode('utf-8')
                if hasattr(e, 'errno'):
                    if e.errno == 17:
                        errorNo = 0
                    elif e.errno == 13:
                        errorNo = 103
                    elif e.errno == 36 or e.errno == 2 or e.errno == 22:
                        errorNo = 102
                else:
                    errorNo = 110

        else:
            errorNo = 102
        return self.sendErrorNode(errorNo, errorMsg)

    def createServerFolder(self, folderPath):
        """Purpose: physically creates a folder on the server"""
        try:
            permissions = Config.ChmodOnFolderCreate
            if not permissions:
                os.makedirs(folderPath)
        except AttributeError:
            permissions = 493

        if permissions:
            oldumask = os.umask(0)
            os.makedirs(folderPath, mode=493)
            os.umask(oldumask)


class UploadFileCommandMixin(object):

    def uploadFile(self, resourceType, currentFolder):
        """
                Purpose: command to upload files to server (same as FileUpload)
                """
        errorNo = 0
        if self.request.has_key('NewFile'):
            newFile = self.request.get('NewFile', '')
            newFileName = newFile.filename
            newFileName = sanitizeFileName(newFileName)
            newFileNameOnly = removeExtension(newFileName)
            newFileExtension = getExtension(newFileName).lower()
            allowedExtensions = Config.AllowedExtensions[resourceType]
            deniedExtensions = Config.DeniedExtensions[resourceType]
            if allowedExtensions:
                isAllowed = False
                if newFileExtension in allowedExtensions:
                    isAllowed = True
            elif deniedExtensions:
                isAllowed = True
                if newFileExtension in deniedExtensions:
                    isAllowed = False
            else:
                isAllowed = True
            if isAllowed:
                currentFolderPath = mapServerFolder(self.userFilesFolder, currentFolder)
                i = 0
                while True:
                    newFilePath = os.path.join(currentFolderPath, newFileName)
                    if os.path.exists(newFilePath):
                        i += 1
                        newFileName = '%s(%d).%s' % (
                         newFileNameOnly, i, newFileExtension)
                        errorNo = 201
                    else:
                        fout = file(newFilePath, 'wb')
                        while True:
                            chunk = newFile.file.read(100000)
                            if not chunk:
                                break
                            fout.write(chunk)

                        fout.close()
                        if os.path.exists(newFilePath):
                            doChmod = False
                            try:
                                doChmod = Config.ChmodOnUpload
                                permissions = Config.ChmodOnUpload
                            except AttributeError:
                                doChmod = True
                                permissions = 493
                            else:
                                if doChmod:
                                    oldumask = os.umask(0)
                                    os.chmod(newFilePath, permissions)
                                    os.umask(oldumask)
                        newFileUrl = combinePaths(self.webUserFilesFolder, currentFolder) + newFileName
                        return self.sendUploadResults(errorNo, newFileUrl, newFileName)

            else:
                return self.sendUploadResults(errorNo=202, customMsg='')
        else:
            return self.sendUploadResults(errorNo=202, customMsg='No File')