# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/lsam/sam_api.py
# Compiled at: 2020-03-19 01:47:03
import sys, re, logging, socket, errno
from lxml import etree, objectify
from .request import SOAPClient, SOAPError, SOAPCommunicationError
unicode_str = unicode if sys.version_info[0] == 2 else str
log = logging.getLogger('lsam')
XMLAPI_NAMESPACE = 'xmlapi_1.0'
XMLAPI_NS = '{' + XMLAPI_NAMESPACE + '}'
API = objectify.ElementMaker(annotate=False, namespace=XMLAPI_NAMESPACE, nsmap={None: XMLAPI_NAMESPACE})

def xmlbool(value):
    if value:
        return 'true'
    return 'false'


class SAMError(SOAPError):
    pass


class SAMException(SAMError):

    def __init__(self, message, node):
        SAMError.__init__(self, message)
        self.node = node


class _notset(object):
    pass


class SAMClient(SOAPClient):
    """
    Simple SAMClient - only supports a single server, requires user build URL.
    """

    def __init__(self, url, username='', password='', size_limit=None, timeout=None):
        SOAPClient.__init__(self, url, size_limit=size_limit, timeout=timeout)
        self.username = username
        self.password = password

    def build_header(self, request_id=None, username=_notset, password=_notset):
        header = API.header(API.security(API.user(self.username if username is _notset else username), API.password(self.password if password is _notset else password)))
        if request_id:
            header.append(API.requestID(request_id))
        return header

    def request(self, body, **kw):
        header = self.build_header(**kw)
        return SOAPClient.request(self, header, body)


SAM = SAMClient

def sam_failed_over(e):
    print e.code
    if e.code in (404, 405):
        return True
    if isinstance(e.code, socket.error) and e.code.errno == errno.ECONNREFUSED:
        return True
    return False


class SAMClientFailover(object):
    """
    SAM SOAP API client

    Host can be a simple hostname, hostname:port, or a fail-over 
    pair: primary:port,secondary:port

    Fail-over occurs when the currently-active host returns a 404 error in
    response to a request. The request is reissued to the standby host.
    """

    def __init__(self, host, username='', password='', size_limit=None, timeout=None):
        try:
            self.active_host, self.standby_host = re.split('\\s*,\\s*', host)
        except ValueError:
            self.active_host, self.standby_host = host, None

        self.username = username
        self.password = password
        self.size_limit = size_limit
        self.timeout = timeout
        self.init_client()
        return

    def init_client(self):
        url = 'http://%s/xmlapi/invoke' % self.active_host
        self.client = SAMClient(url, self.username, self.password, size_limit=self.size_limit, timeout=self.timeout)

    @property
    def last_request(self):
        return self.client.last_request

    @property
    def last_result(self):
        return self.client.last_result

    @property
    def last_length(self):
        return self.client.last_length

    def request(self, body, **kw):
        try:
            return self.client.request(body, **kw)
        except SOAPCommunicationError as e:
            if self.standby_host:
                if not sam_failed_over(e):
                    log.exception('Unexpected SOAPCommunicationError')
                log.warning('SAM failed over from %s to %s' % (
                 self.active_host, self.standby_host))
                self.active_host, self.standby_host = self.standby_host, self.active_host
                self.init_client()
                return self.client.request(body, **kw)
            raise


class XMLBase(object):

    def __str__(self):
        return etree.tostring(self.xml, pretty_print=True, encoding=unicode_str)

    def append(self, xml):
        self.xml.append(xml)

    def tag(self, key, value):
        self.xml.append(getattr(API, key)(value))

    def actionMask(self, actions):
        self.xml.actionMask = ActionMask(actions).xml


class BitMask(XMLBase):
    TAG = None
    VALID_OPTIONS = set()
    INVALID_EMPTY = True

    def __init__(self, options):
        name = self.TAG or self.__class__.__name__
        options = set(options.split('|'))
        invalid_options = options - self.VALID_OPTIONS
        if self.INVALID_EMPTY and not options:
            raise ValueError('%s: no options specified' % name)
        if invalid_options:
            raise ValueError('%s: invalid options: %s' % (
             name, (', ').join(sorted(invalid_options))))
        self.xml = getattr(API, name)()
        for option in sorted(options):
            self.xml.append(API.bit(option))


class ActionMask(BitMask):
    VALID_OPTIONS = set(('create', 'modify', 'delete', 'reset'))


class XMLRequest(XMLBase):
    METHOD = NotImplemented

    def __init__(self):
        self.xml = getattr(API, self.METHOD)()

    def request(self, conn, **kw):
        response = conn.request(self.xml, **kw)
        for node in response.iterchildren():
            if node.tag.endswith('Exception'):
                raise SAMException(str(node.description), node)

        for node in response.iterchildren():
            if node.tag.endswith('Response'):
                return node
            raise SAMError('Unknown response tag: <%s>' % node.tag)


class FilterExpr(XMLBase):

    def __init__(self, tag=None):
        self.xml = getattr(API, tag or 'and')()

    def subexpr(self, conjunction=None):
        if conjunction is None:
            conjunction = 'or' if self.xml.tag == 'and' else 'and'
        filter = FilterExpr(conjunction)
        self.xml.append(filter.xml)
        return filter

    def equal(self, attr, value):
        self.xml.append(API.equal(name=attr, value=value))

    def gt(self, attr, value):
        self.xml.append(API.greater(name=attr, value=value))

    def ge(self, attr, value):
        self.xml.append(API.greaterOrEqual(name=attr, value=value))

    def lt(self, attr, value):
        self.xml.append(API.less(name=attr, value=value))

    def le(self, attr, value):
        self.xml.append(API.lessOrEqual(name=attr, value=value))

    def wildcard(self, attr, pattern):
        self.xml.append(API.wildcard(name=attr, value=pattern))

    def between(self, attr, first, second):
        self.xml.append(API.between(name=attr, first=first, second=second))


RequestFilter = FilterExpr

class Filter(XMLBase):

    def __init__(self, conjunction=None, className=None, childClass=None, withChildrenOnly=None):
        self.conjunction = (conjunction or 'and').lower()
        kw = {}
        if className:
            kw['class'] = className
            if childClass:
                kw['childClass'] = childClass
            if withChildrenOnly is not None:
                kw['withChildrenOnly'] = xmlbool(withChildrenOnly)
        self.xml = API.filter(**kw)
        self.children_xml = None
        self.expr = None
        return

    def children(self, className, childClass, withChildrenOnly=False):
        if self.children_xml is None:
            self.children_xml = API.children()
            self.xml.append(self.children_xml)
        filter = Filter(className=className, childClass=childClass, withChildrenOnly=withChildrenOnly)
        self.children_xml.append(filter.xml)
        return filter

    def __getattr__(self, attr):
        if attr not in FilterExpr.__dict__:
            raise AttributeError(attr)
        if self.expr is None:
            self.expr = FilterExpr(self.conjunction)
            self.xml.append(self.expr.xml)
        return getattr(self.expr, attr)


class ResultFilter(XMLBase):

    def __init__(self, className=None):
        attrs = {}
        if className:
            attrs['class'] = className
        self.xml = API.resultFilter(**attrs)
        self._children = None
        return

    def fields(self, *names):
        for name in names:
            self.xml.append(API.attribute(name))

    def __init_children(self):
        if self._children is None:
            children = API.children()
            self.xml.children = []
            self.xml.append(children)
            self._children = children
        return

    def no_children(self):
        self.xml.children = API.children()

    def children(self, className=None):
        if not hasattr(self.xml, 'children'):
            self.xml.children = API.children()
        child = ResultFilter(className)
        self.xml.children.append(child.xml)
        return child