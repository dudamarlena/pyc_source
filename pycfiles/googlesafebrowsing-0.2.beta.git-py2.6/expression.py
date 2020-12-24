# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/googlesafebrowsing/expression.py
# Compiled at: 2010-12-12 06:18:52
"""Helper classes which help converting a url to a list of SB expressions."""
import array, logging, re, string, urllib, urlparse, util

class UrlParseError(Exception):
    pass


def GenerateSafeChars():
    """
  Return a string containing all 'safe' characters that shouldn't be escaped
  for url encoding. This includes all printable characters except '#%' and
  whitespace characters.
  """
    unfiltered_chars = string.digits + string.ascii_letters + string.punctuation
    filtered_list = [ c for c in unfiltered_chars if c not in '%#' ]
    return array.array('c', filtered_list).tostring()


class ExpressionGenerator(object):
    """Class does the conversion url -> list of SafeBrowsing expressions.

  This class converts a given url into the list of all SafeBrowsing host-suffix,
  path-prefix expressions for that url.  These are expressions that are on the
  SafeBrowsing lists.
  """
    HEX = re.compile('^0x([a-fA-F0-9]+)$')
    OCT = re.compile('^0([0-7]+)$')
    DEC = re.compile('^(\\d+)$')
    IP_WITH_TRAILING_SPACE = re.compile('^(\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}) ')
    POSSIBLE_IP = re.compile('^(?i)((?:0x[0-9a-f]+|[0-9\\\\.])+)$')
    FIND_BAD_OCTAL_REGEXP = re.compile('(^|\\.)0\\d*[89]')
    HOST_PORT_REGEXP = re.compile('^(?:.*@)?(?P<host>[^:]*)(:(?P<port>\\d+))?$')
    SAFE_CHARS = GenerateSafeChars()
    DEFAULT_PORTS = {'http': '80', 'https': '443', 'ftp': '21'}

    def __init__(self, url):
        parse_exception = UrlParseError('failed to parse URL "%s"' % (url,))
        canonical_url = ExpressionGenerator.CanonicalizeUrl(url)
        if not canonical_url:
            raise parse_exception
        self._host_lists = []
        self._path_exprs = []
        url_split = urlparse.urlsplit(canonical_url)
        canonical_host, canonical_path = url_split[1], url_split[2]
        self._MakeHostLists(canonical_host, parse_exception)
        if url_split[3]:
            self._path_exprs.append(canonical_path + '?' + url_split[3])
        self._path_exprs.append(canonical_path)
        path_parts = canonical_path.rstrip('/').lstrip('/').split('/')[:3]
        if canonical_path.count('/') < 4:
            path_parts.pop()
        while path_parts:
            self._path_exprs.append('/' + ('/').join(path_parts) + '/')
            path_parts.pop()

        if canonical_path != '/':
            self._path_exprs.append('/')

    @staticmethod
    def CanonicalizeUrl(url):
        """Canonicalize the given URL for the SafeBrowsing protocol.

    Args:
      url: URL to canonicalize.
    Returns:
      A canonical URL or None if the URL could not be canonicalized.
    """
        tmp_pos = url.find('#')
        if tmp_pos >= 0:
            url = url[0:tmp_pos]
        url = url.lstrip().rstrip()
        url = url.replace('\t', '').replace('\r', '').replace('\n', '')
        url = ExpressionGenerator._Escape(url)
        url_split = urlparse.urlsplit(url)
        if not url_split[0]:
            url = 'http://' + url
            url_split = urlparse.urlsplit(url)
        url_scheme = url_split[0].lower()
        if url_scheme not in ExpressionGenerator.DEFAULT_PORTS:
            return None
        else:
            m = ExpressionGenerator.HOST_PORT_REGEXP.match(url_split[1])
            if not m:
                return None
            host, port = m.group('host'), m.group('port')
            canonical_host = ExpressionGenerator.CanonicalizeHost(host)
            if not canonical_host:
                return None
            if port and port != ExpressionGenerator.DEFAULT_PORTS[url_scheme]:
                canonical_host += ':' + port
            canonical_path = ExpressionGenerator.CanonicalizePath(url_split[2])
            canonical_url = url_split[0] + '://' + canonical_host + canonical_path
            if url_split[3] != '' or url.endswith('?'):
                canonical_url += '?' + url_split[3]
            return canonical_url

    @staticmethod
    def CanonicalizePath(path):
        """Canonicalize the given path."""
        if not path:
            return '/'
        if path[0] != '/':
            path = '/' + path
        path = ExpressionGenerator._Escape(path)
        path_components = []
        for path_component in path.split('/'):
            if path_component == '..':
                if len(path_components) > 0:
                    path_components.pop()
            elif path_component != '.' and path_component != '':
                path_components.append(path_component)

        canonical_path = '/' + ('/').join(path_components)
        if path.endswith('/') and not canonical_path.endswith('/'):
            canonical_path += '/'
        return canonical_path

    @staticmethod
    def CanonicalizeHost(host):
        """Canonicalize the given host. Returns None in case of an error."""
        if not host:
            return None
        else:
            host = ExpressionGenerator._Escape(host.lower())
            ip = ExpressionGenerator.CanonicalizeIp(host)
            if ip:
                host = ip
            else:
                host_split = [ part for part in host.split('.') if part ]
                if len(host_split) < 2:
                    return None
                host = ('.').join(host_split)
            return host

    @staticmethod
    def CanonicalizeIp(host):
        """
    Return a canonicalized IP if host can represent an IP and None otherwise.
    """
        if len(host) <= 15:
            m = ExpressionGenerator.IP_WITH_TRAILING_SPACE.match(host)
            if m:
                host = m.group(1)
        if not ExpressionGenerator.POSSIBLE_IP.match(host):
            return
        else:
            allow_octal = not ExpressionGenerator.FIND_BAD_OCTAL_REGEXP.search(host)
            host_split = [ part for part in host.split('.') if part ]
            if len(host_split) > 4:
                return
            ip = []
            for i in xrange(len(host_split)):
                m = ExpressionGenerator.HEX.match(host_split[i])
                if m:
                    base = 16
                else:
                    m = ExpressionGenerator.OCT.match(host_split[i])
                    if m and allow_octal:
                        base = 8
                    else:
                        m = ExpressionGenerator.DEC.match(host_split[i])
                        if m:
                            base = 10
                        else:
                            return
                n = long(m.group(1), base)
                if n > 255:
                    if i < len(host_split) - 1:
                        n &= 255
                        ip.append(n)
                    else:
                        bytes = []
                        shift = 0
                        while n > 0 and len(bytes) < 4:
                            bytes.append(n & 255)
                            n >>= 8

                        if len(ip) + len(bytes) > 4:
                            return
                        bytes.reverse()
                        ip.extend(bytes)
                else:
                    ip.append(n)

            while len(ip) < 4:
                ip.append(0)

            return '%u.%u.%u.%u' % tuple(ip)

    def Expressions(self):
        """
    A generator of the possible expressions.
    """
        for host_parts in self._host_lists:
            host = ('.').join(host_parts)
            for p in self._path_exprs:
                yield Expression(host, p)

    @staticmethod
    def _Escape(unescaped_str):
        """Fully unescape the given string, then re-escape once.

    Args:
      unescaped_str: string that should be escaped.
    Returns:
      Escaped string according to the SafeBrowsing protocol.
    """
        unquoted = urllib.unquote(unescaped_str)
        while unquoted != unescaped_str:
            unescaped_str = unquoted
            unquoted = urllib.unquote(unquoted)

        return urllib.quote(unquoted, ExpressionGenerator.SAFE_CHARS)

    def _MakeHostLists(self, host, parse_exception):
        """
    Canonicalize host and build self._host_lists.
    """
        ip = ExpressionGenerator.CanonicalizeIp(host)
        if ip is not None:
            self._host_lists.append([ip])
            return
        else:
            host_split = [ part for part in host.split('.') if part ]
            if len(host_split) < 2:
                raise parse_exception
            start = len(host_split) - 5
            stop = len(host_split) - 1
            if start <= 0:
                start = 1
            self._host_lists.append(host_split)
            for i in xrange(start, stop):
                self._host_lists.append(host_split[i:])

            return


class Expression(object):
    """Class which represents a host-suffix, path-prefix expression."""

    def __init__(self, host, path):
        self._host = host
        self._path = path
        self._value = host + path
        self._hash_value = util.GetHash256(self._value)

    def __str__(self):
        return self.Value()

    def __repr__(self):
        """
    Not really a good repr. This is for debugging.
    """
        return self.Value()

    def Value(self):
        return self._value

    def HashValue(self):
        return self._hash_value