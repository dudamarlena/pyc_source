# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\mcs\repositories.py
# Compiled at: 2011-12-13 12:34:45
from __future__ import with_statement
import base64, HTMLParser, httplib2, logging, os, urlparse, urllib
logging.basicConfig(level=logging.WARNING, format='%(levelname)s: %(message)s')
log = logging.getLogger('mcs')

class LinkExtractor(HTMLParser.HTMLParser):

    def reset(self):
        HTMLParser.HTMLParser.reset(self)
        self.links = []

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            self.links.extend(value for name, value in attrs if name == 'href')


class RepositoryException(Exception):
    pass


class McRepository(object):

    def __init__(self, *args, **kwargs):
        raise NotImplementedError

    def list_items(self):
        raise NotImplementedError

    def load_item(self, name):
        raise NotImplementedError

    def store_item(self, name, data):
        raise NotImplementedError

    def _filter_items(self, item_list):
        return [ name for name in item_list if name.endswith('.mcz') or name.endswith('.mcd')
               ]

    @staticmethod
    def for_url(url):
        if url.startswith('http:') or url.startswith('https:'):
            return McHttpRepository(url)
        if url.partition(':')[0] in McHttpRepositoryShortcut.locations:
            return McHttpRepositoryShortcut(url)
        return McLocalRepository(url)


class McLocalRepository(McRepository):

    def __init__--- This code section failed: ---

 L.  56         0  LOAD_GLOBAL           0  'os'
                3  LOAD_ATTR             1  'path'
                6  LOAD_ATTR             2  'abspath'
                9  LOAD_FAST             1  'path'
               12  CALL_FUNCTION_1       1  None
               15  LOAD_FAST             0  'self'
               18  STORE_ATTR            1  'path'

 L.  57        21  LOAD_GLOBAL           0  'os'
               24  LOAD_ATTR             1  'path'
               27  LOAD_ATTR             3  'exists'
               30  LOAD_FAST             0  'self'
               33  LOAD_ATTR             1  'path'
               36  CALL_FUNCTION_1       1  None
               39  POP_JUMP_IF_FALSE    63  'to 63'
               42  LOAD_GLOBAL           0  'os'
               45  LOAD_ATTR             1  'path'
               48  LOAD_ATTR             4  'isdir'
               51  LOAD_FAST             0  'self'
               54  LOAD_ATTR             1  'path'
               57  CALL_FUNCTION_1       1  None
             60_0  COME_FROM            39  '39'
               60  POP_JUMP_IF_TRUE     79  'to 79'
               63  LOAD_ASSERT              AssertionError
               66  LOAD_CONST               "'%s' does not exist or is not a directory."
               69  LOAD_FAST             0  'self'
               72  LOAD_ATTR             1  'path'
               75  BINARY_MODULO    
               76  RAISE_VARARGS_2       2  None

Parse error at or near `BINARY_MODULO' instruction at offset 75

    def list_items(self):
        return self._filter_items(os.listdir(self.path))

    def load_item(self, name):
        with file(os.path.join(self.path, name), 'rb') as (f):
            return f.read()

    def store_item(self, name, data):
        with file(os.path.join(self.path, name), 'wb') as (f):
            f.write(data)


class McHttpRepository(McRepository):

    def __init__(self, url):
        self.http = httplib2.Http()
        self.additional_headers = dict()
        urlsplit = urlparse.urlsplit(url)
        if urlsplit.username or urlsplit.password:
            self.url = urlparse.urlunsplit([
             urlsplit[0],
             (urlsplit.port or urlsplit).hostname if 1 else '%s:%i' % (urlsplit.hostname, urlsplit.port),
             urlsplit[2],
             urlsplit[3],
             urlsplit[4]])
            self.set_credentials(urlsplit.username, urlsplit.password)
        else:
            self.url = urlparse.urlunsplit(urlsplit)

    def set_credentials(self, username, password):
        self.additional_headers['authorization'] = 'Basic: %s' % base64.b64encode('%s:%s' % (username, password))

    def list_items(self):
        resp, data = self.http.request(self.url, headers=self.additional_headers)
        if not 200 <= resp.status <= 299:
            raise RepositoryException('Could not load version list: HTTP error %i (%s)' % (resp.status, resp.reason))
        link_extractor = LinkExtractor()
        link_extractor.feed(data)
        return self._filter_items(link_extractor.links)

    def load_item(self, name):
        resp, data = self.http.request(self._url_from_name(name), headers=self.additional_headers)
        if not 200 <= resp.status <= 299:
            raise RepositoryException('Could not load item: HTTP error %i (%s)' % (resp.status, resp.reason))
        return data

    def store_item(self, name, data):
        resp, data = self.http.request(self._url_from_name(name), method='PUT', body=data, headers=self.additional_headers)
        if not 200 <= resp.status <= 299:
            raise RepositoryException('Could not store item: HTTP error %i (%s)' % (resp.status, resp.reason))

    def _url_from_name(self, name):
        return urlparse.urljoin(self.url, urllib.quote(name))


class McHttpRepositoryShortcut(McHttpRepository):
    locations = dict(hpi='http://www.hpi.uni-potsdam.de/hirschfeld/squeaksource/%s/', lukas='http://source.lukas-renggli.ch/%s/', squeak='http://source.squeak.org/%s/', squeakfoundation='http://source.squeakfoundation.org/%s/', ss='http://www.squeaksource.com/%s/', wiresong='http://source.wiresong.ca/%s/')

    def __init__(self, url):
        base, identifier = url.split(':', 1)
        if base not in self.locations:
            raise RepositoryException('Unknown shortcut: %s', base)
        credentials, _, position = identifier.rpartition('@')
        super(McHttpRepositoryShortcut, self).__init__(self.locations[base] % position)
        if credentials:
            self.set_credentials(*credentials.split(':', 1))