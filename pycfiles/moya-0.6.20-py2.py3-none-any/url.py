# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/will/projects/moya/moya/url.py
# Compiled at: 2016-09-16 18:15:15
"""
A moya context object to represent a URL

"""
from __future__ import unicode_literals
from __future__ import print_function
from .containers import QueryData
from .urltools import urlencode
from .interface import AttributeExposer
from .compat import implements_to_string, text_type, PY2
if PY2:
    from urlparse import urlsplit, urlunsplit, urljoin
else:
    from urllib.parse import urlsplit, urlunsplit, urljoin

def get_domain(url):
    """Get a domain from a URL or empty string"""
    if not isinstance(url, text_type):
        return b''
    netloc = urlsplit(url).netloc
    if b':' in netloc:
        domain = netloc.split(b':', 1)[0]
    else:
        domain = netloc
    return domain


class _Exposed(object):

    def __init__(self, name):
        self.attribute_name = b'_' + name

    def __get__(self, obj, objtype):
        return getattr(obj, self.attribute_name)

    def __set__(self, obj, val):
        setattr(obj, self.attribute_name, val)


@implements_to_string
class URL(AttributeExposer):
    __moya_exposed_attributes__ = [b'scheme',
     b'netloc',
     b'path',
     b'qs',
     b'query',
     b'fragment',
     b'base',
     b'no_fragment',
     b'no_scheme',
     b'with_slash',
     b'parent_dir',
     b'resource']

    def __init__(self, url):
        super(URL, self).__init__()
        self._url = text_type(url)
        split_url = urlsplit(url, allow_fragments=True)
        self._scheme, self._netloc, self._path, self._qs, self._fragment = split_url
        self._query_dict = QueryData.from_qs(self._qs, change_callback=self._changed)

    scheme = _Exposed(b'scheme')
    netloc = _Exposed(b'netloc')
    path = _Exposed(b'path')
    qs = _Exposed(b'qs')
    fragment = _Exposed(b'fragment')

    def _changed(self):
        self._modified = True

    def __repr__(self):
        return (b'<URL "{}">').format(self)

    def __str__(self):
        self._qs = text_type(self._query_dict)
        parts = (self.scheme,
         self.netloc,
         self.path,
         self.qs,
         self.fragment)
        return urlunsplit(parts)

    def __moyaconsole__(self, console):
        console(self.scheme + b'://', fg=b'blue')(self.netloc, fg=b'green')(self.path, italic=True)
        if self.qs:
            console(b'?' + self.qs, fg=b'blue', bold=True)
        if self.fragment:
            console(b'#' + self.fragment, fg=b'magenta', bold=True)
        console.nl()

    def __moyarepr__(self, context):
        return (b"url:'{}'").format(text_type(self))

    def join(self, path):
        return URL(urljoin(self, path))

    def __truediv__(self, path):
        return self.join(text_type(path))

    def __div__(self, path):
        return self.join(text_type(path))

    @property
    def base(self):
        parts = (self.scheme,
         self.netloc,
         self.path,
         b'',
         b'')
        return URL(urlunsplit(parts))

    @property
    def no_fragment(self):
        parts = (self.scheme,
         self.netloc,
         self.path,
         self.qs,
         b'')
        return URL(urlunsplit(parts))

    @property
    def no_scheme(self):
        parts = (b'',
         self.netloc,
         self.path,
         self.qs,
         self.fragment)
        return URL(urlunsplit(parts))

    @property
    def parent_dir(self):
        path = (b'/').join(self.path.rstrip(b'/').split(b'/')[:-1]) + b'/'
        parts = (self.scheme,
         self.netloc,
         path,
         self.qs,
         self.fragment)
        return URL(urlunsplit(parts))

    @property
    def with_slash(self):
        parts = (self.scheme,
         self.netloc,
         self.path.rstrip(b'/') + b'/',
         self.qs,
         self.fragment)
        return URL(urlunsplit(parts))

    @property
    def qs(self):
        return self._qs

    @property
    def query(self):
        return self._query_dict

    @property
    def resource(self):
        return self.path.rsplit(b'/', 1)[(-1)]


if __name__ == b'__main__':
    url = URL(b'http://moyaroject.com/foo/bar/baz')
    url.query[b'test'] = b'bar'
    print(url)
    url = URL(b'/foo/bar')
    print(url)
    url.query.update({b'foo': b'bar'})
    print(url)