# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/lsam/request.py
# Compiled at: 2019-11-25 19:59:00
try:
    from urllib.request import Request, urlopen
    from urllib.error import HTTPError, URLError
except ImportError:
    from urllib2 import Request, urlopen, HTTPError, URLError

from lxml import etree, objectify
SOAP_NAMESPACE = 'http://schemas.xmlsoap.org/soap/envelope/'
SOAP_NS = '{' + SOAP_NAMESPACE + '}'
SOAP = objectify.ElementMaker(annotate=False, namespace=SOAP_NAMESPACE, nsmap={'SOAP': SOAP_NAMESPACE})

class SOAPError(Exception):

    def __init__(self, message):
        Exception.__init__(self, message)
        self.message = message


class SOAPLimit(SOAPError):
    pass


class SOAPParseError(SOAPError):
    pass


class SOAPFault(SOAPError):
    pass


class SOAPCommunicationError(SOAPError):

    def __init__(self, reason, code=None):
        SOAPError.__init__(self, reason)
        self.code = code


class _ByteCounterProxy(object):
    __slots__ = ('count', 'file', 'limit')

    def __init__(self, file, limit=None):
        self.file = file
        self.limit = limit
        self.count = 0

    def read(self, *a):
        data = self.file.read(*a)
        self.count += len(data)
        if self.limit is not None and self.count > self.limit:
            raise SOAPLimit('SOAP response exceeds %s byte limit' % self.limit)
        return data

    def close(self):
        self.file.close()


class SOAPClient(object):
    """
    Generic SOAP request handler
    """

    def __init__(self, url, recover=False, user_agent='lsam', size_limit=None, timeout=None):
        self.url = url
        self.recover = recover
        self.user_agent = user_agent
        self.size_limit = size_limit or None
        self.timeout = timeout or None
        self.last_request = None
        self.last_result = None
        self.last_length = None
        return

    def request(self, header, body):
        request = SOAP.Envelope(SOAP.Header(header), SOAP.Body(body))
        self.last_request = request
        req = Request(self.url)
        req.add_header('User-Agent', self.user_agent)
        req.add_header('Content-type', 'text/xml; charset="UTF-8"')
        req.add_header('SOAPAction', '""')
        req.data = etree.tostring(request)
        try:
            conn = _ByteCounterProxy(urlopen(req, timeout=self.timeout))
        except HTTPError as e:
            raise SOAPCommunicationError('%s: %s' % (self.url, e), code=e.code)
        except URLError as e:
            raise SOAPCommunicationError('%s: %s' % (self.url, e), code=e.reason)

        try:
            parser = objectify.makeparser(recover=self.recover)
            try:
                result = objectify.parse(conn, parser)
            except URLError as e:
                raise SOAPCommunicationError('%s: %s' % (self.url, e))
            except etree.Error as e:
                raise SOAPParseError('%s: %s' % (self.url, e))

        finally:
            conn.close()

        self.last_length = conn.count
        self.last_result = result
        for node in result.getroot().iterchildren():
            tag = node.tag.replace(SOAP_NS, '')
            if tag == 'Header':
                continue
            if tag == 'Body':
                return node
            if tag == 'Fault':
                raise SOAPFault(str(node.find('faultstring')))
            raise SOAPError('Unknown SOAP tag: <%s>' % node.tag)