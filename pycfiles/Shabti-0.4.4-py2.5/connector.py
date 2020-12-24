# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/shabti/templates/moinmoin/+package+/public/moin_static/applets/FCKeditor/editor/filemanager/connectors/py/connector.py
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

See config.py for configuration settings

"""
import os
from fckutil import *
from fckcommands import *
from fckoutput import *
from fckconnector import FCKeditorConnectorBase
import config as Config

class FCKeditorConnector(FCKeditorConnectorBase, GetFoldersCommandMixin, GetFoldersAndFilesCommandMixin, CreateFolderCommandMixin, UploadFileCommandMixin, BaseHttpMixin, BaseXmlMixin, BaseHtmlMixin):
    """The Standard connector class."""

    def doResponse(self):
        """Main function. Process the request, set headers and return a string as response."""
        s = ''
        if not Config.Enabled:
            return self.sendError(1, 'This connector is disabled.  Please check the connector configurations in "editor/filemanager/connectors/py/config.py" and try again.')
        for key in ('Command', 'Type', 'CurrentFolder'):
            if not self.request.has_key(key):
                return

        command = self.request.get('Command')
        resourceType = self.request.get('Type')
        currentFolder = getCurrentFolder(self.request.get('CurrentFolder'))
        if currentFolder is None:
            if command == 'FileUpload':
                return self.sendUploadResults(errorNo=102, customMsg='')
            else:
                return self.sendError(102, '')
        if command not in Config.ConfigAllowedCommands:
            return self.sendError(1, "The %s command isn't allowed" % command)
        if resourceType not in Config.ConfigAllowedTypes:
            return self.sendError(1, 'Invalid type specified')
        if command == 'QuickUpload':
            self.userFilesFolder = Config.QuickUploadAbsolutePath[resourceType]
            self.webUserFilesFolder = Config.QuickUploadPath[resourceType]
        else:
            self.userFilesFolder = Config.FileTypesAbsolutePath[resourceType]
            self.webUserFilesFolder = Config.FileTypesPath[resourceType]
        if not self.userFilesFolder:
            self.userFilesFolder = mapServerPath(self.environ, self.webUserFilesFolder)
        if not os.path.exists(self.userFilesFolder):
            try:
                self.createServerFolder(self.userFilesFolder)
            except:
                return self.sendError(1, 'This connector couldn\'t access to local user\'s files directories.  Please check the UserFilesAbsolutePath in "editor/filemanager/connectors/py/config.py" and try again. ')

        if command == 'FileUpload':
            return self.uploadFile(resourceType, currentFolder)
        url = combinePaths(self.webUserFilesFolder, currentFolder)
        s += self.createXmlHeader(command, resourceType, currentFolder, url)
        selector = {'GetFolders': self.getFolders, 'GetFoldersAndFiles': self.getFoldersAndFiles, 
           'CreateFolder': self.createFolder}
        s += selector[command](resourceType, currentFolder)
        s += self.createXmlFooter()
        return s


if __name__ == '__main__':
    try:
        conn = FCKeditorConnector()
        data = conn.doResponse()
        for header in conn.headers:
            print '%s: %s' % header

        print
        print data
    except:
        print 'Content-Type: text/plain'
        print
        import cgi
        cgi.print_exception()