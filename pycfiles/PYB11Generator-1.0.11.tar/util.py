# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\pyazure\util.py
# Compiled at: 2012-01-28 13:57:35
__doc__ = '\nPython wrapper around Windows Azure storage and management APIs\n\nAuthors:\n    Sriram Krishnan <sriramk@microsoft.com>\n    Steve Marx <steve.marx@microsoft.com>\n    Tihomir Petkov <tpetkov@gmail.com>\n    Blair Bethwaite <blair.bethwaite@gmail.com>\n\nLicense:\n    GNU General Public Licence (GPL)\n    \n    This file is part of pyazure.\n    \n    pyazure is free software: you can redistribute it and/or modify\n    it under the terms of the GNU General Public License as published by\n    the Free Software Foundation, either version 3 of the License, or\n    (at your option) any later version.\n\n    pyazure is distributed in the hope that it will be useful,\n    but WITHOUT ANY WARRANTY; without even the implied warranty of\n    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the\n    GNU General Public License for more details.\n\n    You should have received a copy of the GNU General Public License\n    along with pyazure. If not, see <http://www.gnu.org/licenses/>.\n'
import base64, re, time, math, hmac, hashlib, urllib2, httplib, os.path
from urlparse import urlsplit, urljoin, parse_qs
from datetime import datetime, timedelta
from StringIO import StringIO
import logging
try:
    from collections import OrderedDict
    _builtin_odict = True
except ImportError:
    _builtin_odict = False

try:
    from lxml import etree
except ImportError:
    from xml.etree import ElementTree as etree

log = logging.getLogger('pyazure')
log.setLevel(logging.WARN)
console_handler = logging.StreamHandler()
log.addHandler(console_handler)
SERVICE_MANAGEMENT_HOST = 'management.core.windows.net'
PREFIX_STORAGE_HEADER = 'x-ms-'
PREFIX_PROPERTIES = 'x-ms-prop-'
PREFIX_METADATA = 'x-ms-meta-'
MANAGEMENT_VERSION_HEADER = 'x-ms-version'
MANAGEMENT_VERSION = '2011-10-01'
NEW_LINE = '\n'
TIME_FORMAT = '%a, %d %b %Y %H:%M:%S %Z'
HEADERS_NEXTPARTITIONKEY = PREFIX_STORAGE_HEADER + 'continuation-nextpartitionkey'
HEADERS_NEXTROWKEY = PREFIX_STORAGE_HEADER + 'continuation-nextrowkey'
HEADERS_NEXTTABLENAME = PREFIX_STORAGE_HEADER + 'continuation-nexttablename'
NAMESPACE_M = 'http://schemas.microsoft.com/ado/2007/08/dataservices/metadata'
NAMESPACE_D = 'http://schemas.microsoft.com/ado/2007/08/dataservices'
NAMESPACE_ATOM = 'http://www.w3.org/2005/Atom'
NAMESPACE_MANAGEMENT = 'http://schemas.microsoft.com/windowsazure'
NAMESPACE_SERVICECONFIG = 'http://schemas.microsoft.com/ServiceHosting/2008/10/ServiceConfiguration'
TAGS_ATOM_ENTRY = '{%s}entry' % NAMESPACE_ATOM
TAGS_ATOM_ID = '{%s}id' % NAMESPACE_ATOM
TAGS_ATOM_CONTENT = '{%s}content' % NAMESPACE_ATOM
TAGS_ATOM_ENTRY = '{%s}entry' % NAMESPACE_ATOM
TAGS_ATOM_QUEUEMESSAGE = '{%s}QueueMessage' % NAMESPACE_ATOM
TAGS_ATOM_MESSAGEID = '{%s}MessageId' % NAMESPACE_ATOM
TAGS_ATOM_POPRECEIPT = '{%s}PopReceipt' % NAMESPACE_ATOM
TAGS_ATOM_MESSAGETEXT = '{%s}MessageText' % NAMESPACE_ATOM
TAGS_M_PROPERTIES = '{%s}properties' % NAMESPACE_M
TAGS_D_TABLENAME = '{%s}TableName' % NAMESPACE_D
TAGS_WA_URL = '{%s}Url' % NAMESPACE_MANAGEMENT
TAGS_WA_SERVICENAME = '{%s}ServiceName' % NAMESPACE_MANAGEMENT
ATTRIBUTES_M_TYPE = '{%s}type' % NAMESPACE_M

class WAError(Exception):
    pass


class WASMError(WAError):

    def __init__(self, http_status_code, error_code=None, user_message=None, httperror=None):
        if isinstance(httperror, urllib2.HTTPError):
            self.httperror = httperror
        else:
            self.httperror = None
        self.http_status_code = http_status_code
        self.error_code = error_code
        self.user_message = user_message
        super(WASMError, self).__init__(http_status_code, error_code, user_message)
        return


def add_url_parameter(request_string, key, value):
    separator = '&' if '?' in request_string else '?'
    return '%s%s%s=%s' % (request_string, separator, key, value)


def get_tag_name_without_namespace(tag):
    if '}' in tag:
        return tag.split('}')[(-1)]
    return tag


def parse_edm_datetime(input):
    d = datetime.strptime(input[:input.find('.')], '%Y-%m-%dT%H:%M:%S')
    if input.find('.') != -1:
        d += timedelta(0, 0, int(round(float(input[input.index('.'):-1]) * 1000000)))
    return d


def parse_edm_int32(input):
    return int(input)


def parse_edm_double(input):
    return float(input)


def parse_edm_boolean(input):
    return input.lower() == 'true'


def get_azure_time():
    return time.strftime('%a, %d %b %Y %H:%M:%S GMT', time.gmtime())


def string_to_wasm_label(s):
    if re.match('^[a-z0-9]{3,24}$', s):
        l = s
    else:
        l = base64.b16encode(s)
        if not re.match('^[a-z0-9]{3,24}$', l):
            raise ValueError('label must be between 3 and 24 characters in ' + 'length and use numbers and lower-case letters only')
    return l


def wasm_label_to_string(l):
    try:
        s = base64.b16decode(l)
    except TypeError:
        if re.match('^[a-z0-9]{3,24}$', l):
            s = l
        else:
            raise ValueError('label must be between 3 and 24 characters in ' + 'length and use numbers and lower-case letters only')

    return s


if not _builtin_odict:
    from UserDict import DictMixin

    class OrderedDict(dict, DictMixin):

        def __init__(self, *args, **kwds):
            if len(args) > 1:
                raise TypeError('expected at most 1 arguments, got %d' % len(args))
            try:
                self.__end
            except AttributeError:
                self.clear()

            self.update(*args, **kwds)

        def clear(self):
            self.__end = end = []
            end += [None, end, end]
            self.__map = {}
            dict.clear(self)
            return

        def __setitem__(self, key, value):
            if key not in self:
                end = self.__end
                curr = end[1]
                curr[2] = end[1] = self.__map[key] = [key, curr, end]
            dict.__setitem__(self, key, value)

        def __delitem__(self, key):
            dict.__delitem__(self, key)
            key, prev, next = self.__map.pop(key)
            prev[2] = next
            next[1] = prev

        def __iter__(self):
            end = self.__end
            curr = end[2]
            while curr is not end:
                yield curr[0]
                curr = curr[2]

        def __reversed__(self):
            end = self.__end
            curr = end[1]
            while curr is not end:
                yield curr[0]
                curr = curr[1]

        def popitem(self, last=True):
            if not self:
                raise KeyError('dictionary is empty')
            if last:
                key = reversed(self).next()
            else:
                key = iter(self).next()
            value = self.pop(key)
            return (
             key, value)

        def __reduce__(self):
            items = [ [k, self[k]] for k in self ]
            tmp = (
             self.__map, self.__end)
            del self.__map
            del self.__end
            inst_dict = vars(self).copy()
            self.__map, self.__end = tmp
            if inst_dict:
                return (self.__class__, (items,), inst_dict)
            return (self.__class__, (items,))

        def keys(self):
            return list(self)

        setdefault = DictMixin.setdefault
        update = DictMixin.update
        pop = DictMixin.pop
        values = DictMixin.values
        items = DictMixin.items
        iterkeys = DictMixin.iterkeys
        itervalues = DictMixin.itervalues
        iteritems = DictMixin.iteritems

        def __repr__(self):
            if not self:
                return '%s()' % (self.__class__.__name__,)
            return '%s(%r)' % (self.__class__.__name__, self.items())

        def copy(self):
            return self.__class__(self)

        @classmethod
        def fromkeys(cls, iterable, value=None):
            d = cls()
            for key in iterable:
                d[key] = value

            return d

        def __eq__(self, other):
            if isinstance(other, OrderedDict):
                if len(self) != len(other):
                    return False
                for p, q in zip(self.items(), other.items()):
                    if p != q:
                        return False

                return True
            return dict.__eq__(self, other)

        def __ne__(self, other):
            return not self == other


def retry(retries, delay=2, backoff=2, delay_ceiling=0, percolate_excs=()):
    """Retries a function or method until it returns something True.
    
    delay sets the initial delay, backoff sets by how many times delay should
    lengthen after each failure. delay_ceiling caps the delay period.
    percolate_excs is a tuple of exception types that should be re-raised
    immediately if caught during execution of the decorated function.
    
    Usage:
        @retry(3)
        def might_fail(...):
            ...
        or with lambda functions e.g.
        retry(3)(lambda: False)()"""
    if backoff <= 1:
        raise ValueError('backoff must be greater than 1')
    if retries != float('infinity'):
        retries = math.floor(retries)
    if retries < 1:
        raise ValueError('retries must be 1 or greater')
    if delay <= 0:
        raise ValueError('delay must be greater than 0')
    if delay_ceiling < 0:
        raise ValueError('delay_ceiling must be >= 0')

    def deco_retry(f):

        def f_retry(*args, **kwargs):
            mtries, mdelay = retries, delay
            try:
                rv = f(*args, **kwargs)
                if rv:
                    return rv
            except percolate_excs:
                raise
            except:
                mtries -= 1

            while mtries > 0:
                mtries -= 1
                time.sleep(mdelay)
                mdelay *= backoff
                if delay_ceiling and mdelay > delay_ceiling:
                    mdelay = delay_ceiling
                try:
                    rv = f(*args, **kwargs)
                    if rv:
                        return rv
                except percolate_excs:
                    raise
                except:
                    if mtries == 0:
                        raise

            return False

        return f_retry

    return deco_retry


def build_wasm_request_body(xml_as_odict, builder=None, root=True, indent=0):
    """Takes an OrderedDict and uses it to build an XML doc suitable for
    sending as a request body to the Windows Azure Management Service. This
    makes it possible for clients to compactly specify dynamic requests.
    Returns the doc as a string including the expected doctype declaration."""
    while len(xml_as_odict) > 0:
        k, v = xml_as_odict.popitem(last=False)
        if not builder:
            builder = etree.TreeBuilder()
            builder.start(k, {'xmlns': NAMESPACE_MANAGEMENT})
        else:
            builder.start(k, {})
        if isinstance(v, dict):
            build_wasm_request_body(v, builder, root=False, indent=indent + 2)
        else:
            builder.data(v)
        builder.end(k)

    if root:
        body = '<?xml version="1.0" encoding="utf-8"?>'
        body += etree.tostring(builder.close(), encoding='utf-8')
        body += NEW_LINE
        return body


class RequestWithMethod(urllib2.Request):
    """Subclass urllib2.Request to add the capability of using methods other
    than GET and POST.
    (Thanks to http://benjamin.smedbergs.us/blog/2008-10-21/putting-and-
        deleteing-in-python-urllib2/)"""

    def __init__(self, method, *args, **kwargs):
        self._method = method
        urllib2.Request.__init__(self, *args, **kwargs)

    def get_method(self):
        return self._method


class ServiceManagementEndpoint(object):
    """Base class for the various service management API operation groups."""

    def __init__(self, management_cert_path, subscription_id, management_key_path=None):
        if not os.path.isfile(management_cert_path):
            raise ValueError('Management certificate not readable or not ' + 'a real file', management_cert_path)
        if management_key_path is not None and not os.path.isfile(management_key_path):
            raise ValueError('Management key not readable or not ' + 'a real file', management_key_path)
        self.cert = management_cert_path
        self.key = management_key_path
        self.sub_id = subscription_id
        log.debug('init ServiceManagementEndpoint; cert:%s, key:%s, sub_id:%s', self.cert, self.key, self.sub_id)
        self._cert_handler = HTTPSClientAuthHandler(self.cert, self.key)
        self._opener = urllib2.build_opener(self._cert_handler)
        return

    @property
    def base_url(self):
        return 'https://%s/%s' % (SERVICE_MANAGEMENT_HOST, self.sub_id)

    def urlopen(self, request):
        """Directs urlopen requests to the ServiceManagementEndpoint
        OpenDirector, which handles HTTPS client cert authn for the API.
        Expects a urllib2.Request object."""
        try:
            return self._opener.open(request)
        except urllib2.HTTPError as e:
            if 200 <= e.code < 300:
                return e
            log.warn('HTTP Response: %s %s', e.code, e.msg)
            try:
                self._raise_wa_error(e)
            except WASMError:
                raise
            except Exception:
                log.error("Could't create Windows Azure error exception " + 'following HTTPError:%s%s%s' + 'there was probably a problem querying the service.', os.linesep, str(e), os.linesep)
                raise

    def get_operation_status(self, request_id):
        """The Get Operation Status operation returns the status of the
        specified operation. After calling an asynchronous operation, you
        can call Get Operation Status to determine whether the operation
        has succeeded, failed, or is still in progress."""
        req = RequestWithMethod('GET', 'https://%s/%s/operations/%s' % (
         SERVICE_MANAGEMENT_HOST, self.sub_id, request_id))
        res = self.urlopen(req)
        if not res.code == httplib.OK:
            self._raise_wa_error(res)
        ET = etree.parse(res)
        result = dict()
        result['Status'] = ET.findtext('.//{%s}Status' % NAMESPACE_MANAGEMENT)
        if result['Status'] == 'InProgress':
            return result
        else:
            result['HttpStatusCode'] = ET.findtext('.//{%s}HttpStatusCode' % NAMESPACE_MANAGEMENT)
            try:
                result['HttpStatusCode'] = int(result['HttpStatusCode'])
            except ValueError:
                log.error("Couldn't convert HttpStatusCode: %s, from operation response", result['HttpStatusCode'])

            if result['Status'] == 'Succeeded':
                return result
            error = ET.find('.//{%s}Error' % NAMESPACE_MANAGEMENT)
            if error is not None:
                result['Error'] = WASMError(*self._get_wa_error(ET))
            return result

    def request_done(self, request_id):
        """Poll asynchronous operation status and indicates whether the
        request has completed (True), is still in-progress (False), or failed
        (WASMError exception raised)."""
        op_status = self.get_operation_status(request_id)
        if op_status['Status'] == 'Succeeded':
            return True
        if op_status['Status'] == 'InProgress':
            return False
        raise op_status['Error']

    @retry(float('infinity'), delay_ceiling=20, percolate_excs=WASMError)
    def wait_for_request(self, request_id):
        """Example showing how to repeatedly poll asynchronous operation status
        with retry and backoff provided by retry decorator. Tries forever."""
        return self.request_done(request_id)

    def _get_wa_error(self, response, response_ET=None):
        """Extracts error details from a urlopen response, including extended
        WA error details that might be included in the response body.
        
        response_ET can be passed in if it has already been read from the
        network, to save re-parsing."""
        ET = etree.parse(response) if response_ET is None else response_ET
        if 'Error' in ET.getroot().tag:
            error = ET.getroot()
        else:
            error = ET.find('.//{%s}Error' % NAMESPACE_MANAGEMENT)
        http_status_code = ET.findtext('.//{%s}HttpStatusCode' % NAMESPACE_MANAGEMENT)
        if http_status_code is None:
            http_status_code = response.code
        else:
            http_status_code = int(http_status_code)
        if error is not None:
            wa_code = error.findtext('{%s}Code' % NAMESPACE_MANAGEMENT)
            wa_message = error.findtext('{%s}Message' % NAMESPACE_MANAGEMENT)
        else:
            wa_code, wa_message = (None, None)
        return (http_status_code, wa_code, wa_message)

    def _raise_wa_error(self, response):
        """Raise a WASMError exception populated with values derived from
        _get_wa_error."""
        raise WASMError(httperror=response, *self._get_wa_error(response))


class HTTPSClientAuthHandler(urllib2.HTTPSHandler):

    def __init__(self, cert, key=None):
        urllib2.HTTPSHandler.__init__(self, debuglevel=0)
        self.key = key
        self.cert = cert

    def https_open(self, req):
        if not req.has_header(MANAGEMENT_VERSION_HEADER):
            req.add_header(MANAGEMENT_VERSION_HEADER, MANAGEMENT_VERSION)
        if req.has_data():
            if req.has_header('Content-type'):
                req.add_unredirected_header('Content-type', 'application/xml')
            req.add_header('Content-type', 'application/xml')
        if not req.has_header('Content-type'):
            req.add_header('Content-type', '')
        log.debug('Request: %s; %s; %s; %s; %s;', req.get_method(), req.get_full_url(), req.headers, req.unredirected_hdrs, req.get_data())
        return self.do_open(self.getConnection, req)

    def getConnection(self, host, *args, **kargs):
        return httplib.HTTPSConnection(host, key_file=self.key, cert_file=self.cert)