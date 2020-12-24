# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/shabti/templates/moinmoin/+package+/public/moin_static/applets/FCKeditor/editor/filemanager/connectors/py/fckoutput.py
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
from time import gmtime, strftime
import string

def escape(text, replace=string.replace):
    """
        Converts the special characters '<', '>', and '&'.

        RFC 1866 specifies that these characters be represented
        in HTML as &lt; &gt; and &amp; respectively. In Python
        1.5 we use the new string.replace() function for speed.
        """
    text = replace(text, '&', '&amp;')
    text = replace(text, '<', '&lt;')
    text = replace(text, '>', '&gt;')
    text = replace(text, '"', '&quot;')
    return text


def convertToXmlAttribute(value):
    if value is None:
        value = ''
    return escape(value)


class BaseHttpMixin(object):

    def setHttpHeaders(self, content_type='text/xml'):
        """Purpose: to prepare the headers for the xml to return"""
        self.setHeader('Expires', 'Mon, 26 Jul 1997 05:00:00 GMT')
        self.setHeader('Last-Modified', strftime('%a, %d %b %Y %H:%M:%S GMT', gmtime()))
        self.setHeader('Cache-Control', 'no-store, no-cache, must-revalidate')
        self.setHeader('Cache-Control', 'post-check=0, pre-check=0')
        self.setHeader('Pragma', 'no-cache')
        self.setHeader('Content-Type', content_type + '; charset=utf-8')


class BaseXmlMixin(object):

    def createXmlHeader(self, command, resourceType, currentFolder, url):
        """Purpose: returns the xml header"""
        self.setHttpHeaders()
        s = '<?xml version="1.0" encoding="utf-8" ?>'
        s += '<Connector command="%s" resourceType="%s">' % (
         command,
         resourceType)
        s += '<CurrentFolder path="%s" url="%s" />' % (
         convertToXmlAttribute(currentFolder),
         convertToXmlAttribute(url))
        return s

    def createXmlFooter(self):
        """Purpose: returns the xml footer"""
        return '</Connector>'

    def sendError(self, number, text):
        """Purpose: in the event of an error, return an xml based error"""
        self.setHttpHeaders()
        return '<?xml version="1.0" encoding="utf-8" ?>' + '<Connector>' + self.sendErrorNode(number, text) + '</Connector>'

    def sendErrorNode(self, number, text):
        if number != 1:
            return '<Error number="%s" />' % number
        else:
            return '<Error number="%s" text="%s" />' % (number, convertToXmlAttribute(text))


class BaseHtmlMixin(object):

    def sendUploadResults(self, errorNo=0, fileUrl='', fileName='', customMsg=''):
        self.setHttpHeaders('text/html')
        return '<script type="text/javascript">\n\t\t\t(function(){var d=document.domain;while (true){try{var A=window.parent.document.domain;break;}catch(e) {};d=d.replace(/.*?(?:\\.|$)/,\'\');if (d.length==0) break;try{document.domain=d;}catch (e){break;}}})();\n\n\t\t\twindow.parent.OnUploadCompleted(%(errorNumber)s,"%(fileUrl)s","%(fileName)s","%(customMsg)s");\n\t\t\t</script>' % {'errorNumber': errorNo, 
           'fileUrl': fileUrl.replace('"', '\\"'), 
           'fileName': fileName.replace('"', '\\"'), 
           'customMsg': customMsg.replace('"', '\\"')}