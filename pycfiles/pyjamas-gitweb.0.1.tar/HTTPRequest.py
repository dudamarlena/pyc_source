# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/lib/python2.5/site-packages/pyjamas/HTTPRequest.py
# Compiled at: 2008-09-03 09:02:13
from pyjamas.__pyjamas__ import get_main_frame
import sys
from pyjamas import Cookies

class HTTPRequest:

    def asyncPost(self, user, pwd, url, postData=None, handler=None):
        if postData == None:
            return self.asyncPostImpl(None, None, user, pwd, url)
        return self.asyncPostImpl(user, pwd, url, postData, handler)

    def asyncGet(self, user, pwd, url, handler):
        if url == None:
            return self.asyncGetImpl(None, None, user, pwd)
        return self.asyncGetImpl(user, pwd, url, handler)

    def createXmlHTTPRequest(self):
        return self.doCreateXmlHTTPRequest()

    def doCreateXmlHTTPRequest(self):
        return get_main_frame().get_xml_http_request()

    def onReadyStateChange(self, xmlHttp, event, ignorearg):
        if xmlHttp.props.ready_state != 4:
            return
        localHandler = xmlHttp.handler
        responseText = xmlHttp.props.response_text
        print 'headers', xmlHttp.get_all_response_headers()
        status = xmlHttp.props.status
        handler = None
        xmlHttp = None
        print 'response text', responseText, dir(responseText)
        if status == 200:
            localHandler.onCompletion(responseText)
        else:
            localHandler.onError(responseText, status)
        return

    def asyncPostImpl(self, user, pwd, url, postData, handler):
        xmlHttp = self.doCreateXmlHTTPRequest()
        print 'xmlHttp', user, pwd, url, postData, handler, dir(xmlHttp)
        xmlHttp.open('POST', url, True, '', '')
        xmlHttp.set_request_header('Content-Type', 'text/plain charset=utf-8')
        for c in Cookies.get_crumbs():
            xmlHttp.set_request_header('Set-Cookie', c)
            print 'setting cookie', c

        xmlHttp.connect('browser-event', self.onReadyStateChange)
        xmlHttp.add_event_listener('onreadystatechange')
        xmlHttp.handler = handler
        xmlHttp.send(postData)
        return True
        handler = None
        xmlHttp = None
        localHandler.onError(str(e))
        return False

    def asyncGetImpl(self, user, pwd, url, handler):
        xmlHttp = self.doCreateXmlHTTPRequest()
        print dir(xmlHttp)
        try:
            xmlHttp.open('GET', url, true, None, None)
            xmlHttp.setRequestHeader('Content-Type', 'text/plain charset=utf-8')
            xmlHttp.send('')
            return True
        except:
            del xmlHttp.onreadystatechange
            handler = None
            xmlHttp = None
            localHandler.onError(String(e))
            return False

        return