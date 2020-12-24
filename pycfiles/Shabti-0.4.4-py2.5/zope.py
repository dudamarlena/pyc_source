# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/shabti/templates/moinmoin/+package+/public/moin_static/applets/FCKeditor/editor/filemanager/connectors/py/zope.py
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

Connector for Python and Zope.

This code was not tested at all.
It just was ported from pre 2.5 release, so for further reference see
\\editor\x0cilemanager\x08rowser\\default\\connectors\\py\\connector.py in previous
releases.

"""
from fckutil import *
from connector import *
import config as Config

class FCKeditorConnectorZope(FCKeditorConnector):
    """
        Zope versiof FCKeditorConnector
        """
    __allow_access_to_unprotected_subobjects__ = 1

    def __init__(self, context=None):
        """
                Constructor
                """
        FCKeditorConnector.__init__(self, environ=None)
        self.context = context
        self.request = FCKeditorRequest(context)
        return

    def getZopeRootContext(self):
        if self.zopeRootContext is None:
            self.zopeRootContext = self.context.getPhysicalRoot()
        return self.zopeRootContext

    def getZopeUploadContext(self):
        if self.zopeUploadContext is None:
            folderNames = self.userFilesFolder.split('/')
            c = self.getZopeRootContext()
            for folderName in folderNames:
                if folderName != '':
                    c = c[folderName]

            self.zopeUploadContext = c
        return self.zopeUploadContext

    def setHeader(self, key, value):
        self.context.REQUEST.RESPONSE.setHeader(key, value)

    def getFolders(self, resourceType, currentFolder):
        s = ''
        s += '<Folders>'
        zopeFolder = self.findZopeFolder(resourceType, currentFolder)
        for (name, o) in zopeFolder.objectItems(['Folder']):
            s += '<Folder name="%s" />' % convertToXmlAttribute(name)

        s += '</Folders>'
        return s

    def getZopeFoldersAndFiles(self, resourceType, currentFolder):
        folders = self.getZopeFolders(resourceType, currentFolder)
        files = self.getZopeFiles(resourceType, currentFolder)
        s = folders + files
        return s

    def getZopeFiles(self, resourceType, currentFolder):
        s = ''
        s += '<Files>'
        zopeFolder = self.findZopeFolder(resourceType, currentFolder)
        for (name, o) in zopeFolder.objectItems(['File', 'Image']):
            s += '<File name="%s" size="%s" />' % (
             convertToXmlAttribute(name),
             o.get_size() / 1024 + 1)

        s += '</Files>'
        return s

    def findZopeFolder(self, resourceType, folderName):
        zopeFolder = self.getZopeUploadContext()
        folderName = self.removeFromStart(folderName, '/')
        folderName = self.removeFromEnd(folderName, '/')
        if resourceType != '':
            try:
                zopeFolder = zopeFolder[resourceType]
            except:
                zopeFolder.manage_addProduct['OFSP'].manage_addFolder(id=resourceType, title=resourceType)
                zopeFolder = zopeFolder[resourceType]

        if folderName != '':
            folderNames = folderName.split('/')
            for folderName in folderNames:
                zopeFolder = zopeFolder[folderName]

        return zopeFolder

    def createFolder(self, resourceType, currentFolder):
        zopeFolder = self.findZopeFolder(resourceType, currentFolder)
        errorNo = 0
        errorMsg = ''
        if self.request.has_key('NewFolderName'):
            newFolder = self.request.get('NewFolderName', None)
            zopeFolder.manage_addProduct['OFSP'].manage_addFolder(id=newFolder, title=newFolder)
        else:
            errorNo = 102
        return self.sendErrorNode(errorNo, errorMsg)

    def uploadFile(self, resourceType, currentFolder, count=None):
        zopeFolder = self.findZopeFolder(resourceType, currentFolder)
        file = self.request.get('NewFile', None)
        fileName = self.getFileName(file.filename)
        fileNameOnly = self.removeExtension(fileName)
        fileExtension = self.getExtension(fileName).lower()
        if count:
            nid = '%s.%s.%s' % (fileNameOnly, count, fileExtension)
        else:
            nid = fileName
        title = nid
        try:
            zopeFolder.manage_addProduct['OFSP'].manage_addFile(id=nid, title=title, file=file.read())
        except:
            if count:
                count += 1
            else:
                count = 1
            return self.zopeFileUpload(resourceType, currentFolder, count)

        return self.sendUploadResults(0)


class FCKeditorRequest(object):
    """A wrapper around the request object"""

    def __init__(self, context=None):
        r = context.REQUEST
        self.request = r

    def has_key(self, key):
        return self.request.has_key(key)

    def get(self, key, default=None):
        return self.request.get(key, default)