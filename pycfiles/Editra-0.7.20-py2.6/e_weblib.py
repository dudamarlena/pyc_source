# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/Editra/src/ebmlib/e_weblib.py
# Compiled at: 2010-12-05 17:39:27
"""
Editra Buisness Model Library: Web Utilities

Utility functions for working with web and other networking protocols

"""
__author__ = 'Cody Precord <cprecord@editra.org>'
__svnid__ = '$Id: e_weblib.py 66131 2010-11-13 05:22:48Z CJP $'
__revision__ = '$Revision: 66131 $'
__all__ = [
 'SOAP12Message']
import urllib2, httplib
_SOAP_TPL = '<?xml version="1.0" encoding="utf-8"?>\n<soap12:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap12="http://www.w3.org/2003/05/soap-envelope">\n<soap12:Body>\n    %(msg)s\n</soap12:Body>\n</soap12:Envelope>\n\n'
_SM_TPL = '<?xml version="1.0" encoding="UTF-8"?>\n<SOAP-ENV:Envelope \nSOAP-ENV:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/"  \nxmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/">\n<SOAP-ENV:Body>\n    %(msg)s\n</SOAP-ENV:Body>\n</SOAP-ENV:Envelope>\n'

class SOAP12Message(object):
    """Class for creating and sending a message
    using the SOAP protocol.

    """

    def __init__(self, host, request, msg, action=''):
        """Create the message object
        @param host: host the message will be sent to (url)
        @param request: POST request
        @param msg: XML Body text
        @keyword action: SoapAction

        """
        assert len(host), 'Must specify a valid host'
        super(SOAP12Message, self).__init__()
        self._host = host
        self._request = request
        self._msg = msg
        self._action = action
        self._http = httplib.HTTP(self._host, 80)

    @property
    def MessageBody(self):
        soapmsg = _SOAP_TPL % dict(msg=self._msg)
        soapmsg = soapmsg.replace('\n', '\r\n')
        return soapmsg

    def Send(self):
        """Send the message"""
        soapmsg = self.MessageBody
        self._http.putrequest('POST', self._request)
        self._http.putheader('Host', self._host)
        self._http.putheader('Content-Type', 'application/soap+xml; charset=utf-8')
        self._http.putheader('Content-Length', '%d' % len(soapmsg))
        self._http.putheader('SOAPAction', '"%s"' % self._action)
        self._http.endheaders()
        self._http.send(soapmsg)

    def GetReply(self):
        """Get the reply (may block for a long time)
        @return: (statuscode, statusmessage, header)

        """
        return self._http.getreply()