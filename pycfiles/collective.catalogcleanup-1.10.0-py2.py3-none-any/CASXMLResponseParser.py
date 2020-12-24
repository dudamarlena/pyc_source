# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/collective/cas4plone/CASXMLResponseParser.py
# Compiled at: 2011-01-19 03:43:40
from HTMLParser import HTMLParser, HTMLParseError

class CASXMLResponseParser(HTMLParser):
    """
    Class used to parse XML response from CAS server.
    It currently works with cas server 2.0.12 from yale.

    it works by raising two types of exceptions :
        - "user", username
        - "failure", failure_message
    """
    _user = 0
    _user_data = None
    _failure = 0
    _failure_data = None

    def handle_starttag(self, tag, attrs):
        if tag == 'cas:user' or tag == 'user':
            self._user = 1
        elif tag == 'cas:authenticationfailure' or tag == 'authenticationfailure':
            self._failure = 1
        else:
            self._user = 0
            self._failure = 0

    def handle_data(self, data):
        if self._user == 1:
            self._user_data = (self._user_data or '') + data.strip()
        if self._failure == 1:
            self._failure_data = (self._failure_data or '') + data.strip()

    def handle_endtag(self, tag):
        pass

    def getUser(self):
        return self._user_data

    def getFailure(self):
        return self._failure_data


if __name__ == '__main__':
    xml_ok = "\n        <cas:serviceResponse xmlns:cas='http://www.yale.edu/tp/cas'>\n          <cas:authenticationSuccess>\n            <cas:user>joeblack</cas:user>\n              <cas:proxyGrantingTicket>PGTIOU-84678-8a9d...\n            </cas:proxyGrantingTicket>\n          </cas:authenticationSuccess>\n        </cas:serviceResponse>"
    xml_failure = "\n        <cas:serviceResponse xmlns:cas='http://www.yale.edu/tp/cas'>\n          <cas:authenticationFailure code='INVALID_REQUEST'>\n            'service' and 'ticket' parameters are both required\n          </cas:authenticationFailure>\n        </cas:serviceResponse>"
    try:
        parser = CASXMLResponseParser()
        parser.feed(xml_ok)
        if parser.getUser() == 'joeblack':
            print 'Test getUser    => OK'
        else:
            print 'Test getUser    => FAIL (%s)' % parser.getUser()
        parser = CASXMLResponseParser()
        parser.feed(xml_failure)
        if parser.getFailure() == "'service' and 'ticket' parameters are both required":
            print 'Test getFailure => OK'
        else:
            print 'Test getFailure => FAIL'
    except HTMLParseError, e:
        print 'XML Parsing exception: ' + str(e)