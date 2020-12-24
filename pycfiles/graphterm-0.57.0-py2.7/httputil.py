# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-x86_64/egg/graphterm/bin/tornado/httputil.py
# Compiled at: 2012-01-23 23:44:33
"""HTTP utility code shared by clients and servers."""
import logging, urllib, re
from tornado.util import b, ObjectDict

class HTTPHeaders(dict):
    """A dictionary that maintains Http-Header-Case for all keys.

    Supports multiple values per key via a pair of new methods,
    add() and get_list().  The regular dictionary interface returns a single
    value per key, with multiple values joined by a comma.

    >>> h = HTTPHeaders({"content-type": "text/html"})
    >>> h.keys()
    ['Content-Type']
    >>> h["Content-Type"]
    'text/html'

    >>> h.add("Set-Cookie", "A=B")
    >>> h.add("Set-Cookie", "C=D")
    >>> h["set-cookie"]
    'A=B,C=D'
    >>> h.get_list("set-cookie")
    ['A=B', 'C=D']

    >>> for (k,v) in sorted(h.get_all()):
    ...    print '%s: %s' % (k,v)
    ...
    Content-Type: text/html
    Set-Cookie: A=B
    Set-Cookie: C=D
    """

    def __init__(self, *args, **kwargs):
        dict.__init__(self)
        self._as_list = {}
        self._last_key = None
        self.update(*args, **kwargs)
        return

    def add(self, name, value):
        """Adds a new value for the given key."""
        norm_name = HTTPHeaders._normalize_name(name)
        self._last_key = norm_name
        if norm_name in self:
            dict.__setitem__(self, norm_name, self[norm_name] + ',' + value)
            self._as_list[norm_name].append(value)
        else:
            self[norm_name] = value

    def get_list(self, name):
        """Returns all values for the given header as a list."""
        norm_name = HTTPHeaders._normalize_name(name)
        return self._as_list.get(norm_name, [])

    def get_all(self):
        """Returns an iterable of all (name, value) pairs.

        If a header has multiple values, multiple pairs will be
        returned with the same name.
        """
        for name, list in self._as_list.iteritems():
            for value in list:
                yield (
                 name, value)

    def parse_line(self, line):
        """Updates the dictionary with a single header line.

        >>> h = HTTPHeaders()
        >>> h.parse_line("Content-Type: text/html")
        >>> h.get('content-type')
        'text/html'
        """
        if line[0].isspace():
            new_part = ' ' + line.lstrip()
            self._as_list[self._last_key][(-1)] += new_part
            dict.__setitem__(self, self._last_key, self[self._last_key] + new_part)
        else:
            name, value = line.split(':', 1)
            self.add(name, value.strip())

    @classmethod
    def parse(cls, headers):
        r"""Returns a dictionary from HTTP header text.

        >>> h = HTTPHeaders.parse("Content-Type: text/html\r\nContent-Length: 42\r\n")
        >>> sorted(h.iteritems())
        [('Content-Length', '42'), ('Content-Type', 'text/html')]
        """
        h = cls()
        for line in headers.splitlines():
            if line:
                h.parse_line(line)

        return h

    def __setitem__(self, name, value):
        norm_name = HTTPHeaders._normalize_name(name)
        dict.__setitem__(self, norm_name, value)
        self._as_list[norm_name] = [value]

    def __getitem__(self, name):
        return dict.__getitem__(self, HTTPHeaders._normalize_name(name))

    def __delitem__(self, name):
        norm_name = HTTPHeaders._normalize_name(name)
        dict.__delitem__(self, norm_name)
        del self._as_list[norm_name]

    def __contains__(self, name):
        norm_name = HTTPHeaders._normalize_name(name)
        return dict.__contains__(self, norm_name)

    def get(self, name, default=None):
        return dict.get(self, HTTPHeaders._normalize_name(name), default)

    def update(self, *args, **kwargs):
        for k, v in dict(*args, **kwargs).iteritems():
            self[k] = v

    _NORMALIZED_HEADER_RE = re.compile('^[A-Z0-9][a-z0-9]*(-[A-Z0-9][a-z0-9]*)*$')
    _normalized_headers = {}

    @staticmethod
    def _normalize_name(name):
        """Converts a name to Http-Header-Case.

        >>> HTTPHeaders._normalize_name("coNtent-TYPE")
        'Content-Type'
        """
        try:
            return HTTPHeaders._normalized_headers[name]
        except KeyError:
            if HTTPHeaders._NORMALIZED_HEADER_RE.match(name):
                normalized = name
            else:
                normalized = ('-').join([ w.capitalize() for w in name.split('-') ])
            HTTPHeaders._normalized_headers[name] = normalized
            return normalized


def url_concat(url, args):
    """Concatenate url and argument dictionary regardless of whether
    url has existing query parameters.

    >>> url_concat("http://example.com/foo?a=b", dict(c="d"))
    'http://example.com/foo?a=b&c=d'
    """
    if not args:
        return url
    if url[(-1)] not in ('?', '&'):
        url += '&' if '?' in url else '?'
    return url + urllib.urlencode(args)


class HTTPFile(ObjectDict):
    """Represents an HTTP file. For backwards compatibility, its instance
    attributes are also accessible as dictionary keys.

    :ivar filename:
    :ivar body:
    :ivar content_type: The content_type comes from the provided HTTP header
        and should not be trusted outright given that it can be easily forged.
    """
    pass


def parse_multipart_form_data(boundary, data, arguments, files):
    """Parses a multipart/form-data body.

    The boundary and data parameters are both byte strings.
    The dictionaries given in the arguments and files parameters
    will be updated with the contents of the body.
    """
    if boundary.startswith(b('"')) and boundary.endswith(b('"')):
        boundary = boundary[1:-1]
    if data.endswith(b('\r\n')):
        footer_length = len(boundary) + 6
    else:
        footer_length = len(boundary) + 4
    parts = data[:-footer_length].split(b('--') + boundary + b('\r\n'))
    for part in parts:
        if not part:
            continue
        eoh = part.find(b('\r\n\r\n'))
        if eoh == -1:
            logging.warning('multipart/form-data missing headers')
            continue
        headers = HTTPHeaders.parse(part[:eoh].decode('utf-8'))
        disp_header = headers.get('Content-Disposition', '')
        disposition, disp_params = _parse_header(disp_header)
        if disposition != 'form-data' or not part.endswith(b('\r\n')):
            logging.warning('Invalid multipart/form-data')
            continue
        value = part[eoh + 4:-2]
        if not disp_params.get('name'):
            logging.warning('multipart/form-data value missing name')
            continue
        name = disp_params['name']
        if disp_params.get('filename'):
            ctype = headers.get('Content-Type', 'application/unknown')
            files.setdefault(name, []).append(HTTPFile(filename=disp_params['filename'], body=value, content_type=ctype))
        else:
            arguments.setdefault(name, []).append(value)


def _parseparam(s):
    while s[:1] == ';':
        s = s[1:]
        end = s.find(';')
        while end > 0 and (s.count('"', 0, end) - s.count('\\"', 0, end)) % 2:
            end = s.find(';', end + 1)

        if end < 0:
            end = len(s)
        f = s[:end]
        yield f.strip()
        s = s[end:]


def _parse_header(line):
    """Parse a Content-type like header.

    Return the main content-type and a dictionary of options.

    """
    parts = _parseparam(';' + line)
    key = parts.next()
    pdict = {}
    for p in parts:
        i = p.find('=')
        if i >= 0:
            name = p[:i].strip().lower()
            value = p[i + 1:].strip()
            if len(value) >= 2 and value[0] == value[(-1)] == '"':
                value = value[1:-1]
                value = value.replace('\\\\', '\\').replace('\\"', '"')
            pdict[name] = value

    return (
     key, pdict)


def doctests():
    import doctest
    return doctest.DocTestSuite()


if __name__ == '__main__':
    import doctest
    doctest.testmod()