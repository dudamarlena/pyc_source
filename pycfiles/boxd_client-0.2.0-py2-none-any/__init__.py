# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/boxdotcom/__init__.py
# Compiled at: 2012-01-18 06:51:09
__doc__ = '\nPython bindings for the Box.com API\n\nCopyright (c) 2007 Thomas Van Machelen <thomas dot vanmachelen at gmail dot com>\nCopyright (c) 2007 John Stowers <john dot stowers at gmail dot com>\n\nUpload, handler and XMLNode code adapted from flickrapi:\nCopyright (c) 2007 Brian "Beej Jorgensen" Hall\n\nLicensed under the Apache License, Version 2.0 (the "License");\nyou may not use this file except in compliance with the License.\nYou may obtain a copy of the License at\n\nhttp://www.apache.org/licenses/LICENSE-2.0\n\nUnless required by applicable law or agreed to in writing, software\ndistributed under the License is distributed on an "AS IS" BASIS,\nWITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. \nSee the License for the specific language governing permissions and \nlimitations under the License. \n'
import sys, os, urllib, urllib2, mimetools, mimetypes, webbrowser, xml.dom
from xml.dom.minidom import parseString
__version__ = '0.2.1'

def get_content_type(filename):
    return mimetypes.guess_type(filename)[0] or 'application/octet-stream'


class XMLNode:
    '''XMLNode -- generic class for holding an XML node

    xmlStr = """<xml foo="32">
    <name bar="10">Name0</name>
    <name bar="11" baz="12">Name1</name>
    </xml>"""

    f = XMLNode.parseXML(xmlStr)

    print f.elementName              # xml
    print f['foo']                   # 32
    print f.name                     # [<name XMLNode>, <name XMLNode>]
    print f.name[0].elementName      # name
    print f.name[0]["bar"]           # 10
    print f.name[0].elementText      # Name0
    print f.name[1].elementName      # name
    print f.name[1]["bar"]           # 11
    print f.name[1]["baz"]           # 12

    '''

    def __init__(self):
        """Construct an empty XML node."""
        self.elementName = ''
        self.elementText = ''
        self.attrib = {}
        self.xml = ''

    def __setitem__(self, key, item):
        """Store a node's attribute in the attrib hash."""
        self.attrib[key] = item

    def __getitem__(self, key):
        """Retrieve a node's attribute from the attrib hash."""
        return self.attrib[key]

    @classmethod
    def parseXML(cls, xmlStr, storeXML=False):
        """Convert an XML string into a nice instance tree of XMLNodes.

        xmlStr -- the XML to parse
        storeXML -- if True, stores the XML string in the root XMLNode.xml
        """

        def __parseXMLElement(element, thisNode):
            """Recursive call to process this XMLNode."""
            thisNode.elementName = element.nodeName
            for i in range(element.attributes.length):
                an = element.attributes.item(i)
                thisNode[an.name] = an.nodeValue

            for a in element.childNodes:
                if a.nodeType == xml.dom.Node.ELEMENT_NODE:
                    child = XMLNode()
                    try:
                        list = getattr(thisNode, a.nodeName)
                    except AttributeError:
                        setattr(thisNode, a.nodeName, [])
                    else:
                        list = getattr(thisNode, a.nodeName)
                        list.append(child)
                        __parseXMLElement(a, child)
                elif a.nodeType == xml.dom.Node.TEXT_NODE:
                    thisNode.elementText += a.nodeValue

            return thisNode

        dom = parseString(xmlStr)
        rootNode = XMLNode()
        if storeXML:
            rootNode.xml = xmlStr
        return __parseXMLElement(dom.firstChild, rootNode)


class BoxDotNetError(Exception):
    """Exception class for errors received from Facebook."""


class BoxDotNet(object):
    END_POINT = 'http://www.box.com/api/1.0/rest?'
    RETURN_CODES = {'get_ticket': 'get_ticket_ok', 
       'get_auth_token': 'get_auth_token_ok', 
       'get_account_tree': 'listing_ok', 
       'logout': 'logout_ok', 
       'create_folder': 'create_ok', 
       'upload': 'upload_ok', 
       'delete': 's_delete_node'}

    def __init__(self):
        self.__handlerCache = {}

    @classmethod
    def __url_encode_params(cls, params={}):
        if not isinstance(params, dict):
            raise Exception('You must pass a dictionary!')
        params_list = []
        for (k, v) in params.items():
            if isinstance(v, list):
                params_list.extend([ (k + '[]', x) for x in v ])
            else:
                params_list.append((k, v))

        return urllib.urlencode(params_list)

    @classmethod
    def check_errors(cls, method, xml):
        status = xml.status[0].elementText
        if status == cls.RETURN_CODES[method]:
            return
        raise BoxDotNetError('Box.com returned [%s] for action [%s]' % (status, method))

    def login(self, api_key):
        rsp = self.get_ticket(api_key=api_key)
        ticket = rsp.ticket[0].elementText
        url = 'http://www.box.com/api/1.0/auth/%s' % ticket
        webbrowser.open_new_tab(url)
        rsp = self.get_auth_token(api_key=api_key, ticket=ticket)
        return rsp

    def __getattr__(self, method, **arg):
        """
        Handle all box.com calls
        """
        if not self.__handlerCache.has_key(method):

            def handler(_self=self, _method=method, **arg):
                url = _self.END_POINT
                arg['action'] = _method
                postData = _self.__url_encode_params(params=arg)
                f = urllib.urlopen(url + postData)
                data = f.read()
                f.close()
                xml = XMLNode.parseXML(data, True)
                _self.check_errors(_method, xml)
                return xml

            self.__handlerCache[method] = handler
        return self.__handlerCache[method]

    def upload(self, filename, **arg):
        """
        Upload a file to box.com
        """
        if filename == None:
            raise UploadException('filename OR jpegData must be specified')
        for a in arg:
            if a not in ('api_key', 'auth_token', 'folder_id', 'share'):
                sys.stderr.write('Box.com api: warning: unknown parameter "%s" sent to Box.com.upload\n' % a)

        url = 'http://upload.box.com/api/1.0/upload/%s/%s' % (arg['auth_token'], arg['folder_id'])
        boundary = mimetools.choose_boundary()
        body = ''
        body += '--%s\r\n' % boundary
        body += 'Content-Disposition: form-data; name="share"\r\n\r\n'
        body += '%s\r\n' % arg['share']
        body += '--%s\r\n' % boundary
        body += 'Content-Disposition: form-data; name="file";'
        body += ' filename="%s"\r\n' % filename
        body += 'Content-Type: %s\r\n\r\n' % get_content_type(filename)
        fp = file(filename, 'rb')
        data = fp.read()
        fp.close()
        postData = body.encode('utf_8') + data + ('\r\n--%s--' % boundary).encode('utf_8')
        request = urllib2.Request(url)
        request.add_data(postData)
        request.add_header('Content-Type', 'multipart/form-data; boundary=%s' % boundary)
        response = urllib2.urlopen(request)
        rspXML = response.read()
        return XMLNode.parseXML(rspXML)