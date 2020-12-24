# uncompyle6 version 3.7.4
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: \Ft\Lib\Uri.py
# Compiled at: 2006-10-23 13:02:21
"""
Classes and functions related to URI validation and resolution

APIs that currently differentiate between Unicode and byte strings are
considered to be experimental; do not count on their uniformity between
releases.

Copyright 2005 Fourthought, Inc. (USA).
Detailed license and copyright information: http://4suite.org/COPYRIGHT
Project home, documentation, distributions: http://4suite.org/
"""
from __future__ import generators
import urllib, urllib2, os, sys, re, mimetools, cStringIO
from string import ascii_letters
from Ft.Lib import UriException, ImportUtil
__all__ = [
 'MatchesUriRefSyntax', 'MatchesUriSyntax', 'PercentEncode', 'PercentDecode', 'SplitUriRef', 'UnsplitUriRef', 'SplitAuthority', 'SplitFragment', 'Absolutize', 'Relativize', 'RemoveDotSegments', 'NormalizeCase', 'NormalizePercentEncoding', 'NormalizePathSegments', 'NormalizePathSegmentsInUri', 'UriResolverBase', 'FtUriResolver', 'BASIC_RESOLVER', 'DEFAULT_URI_SCHEMES', 'UrlOpen', 'UrnToPublicId', 'PublicIdToUrn', 'IsAbsolute', 'GetScheme', 'StripFragment', 'OsPathToUri', 'UriToOsPath', 'BaseJoin', 'MakeUrllibSafe', 'WINDOWS_SLASH_COMPAT', 'UriDict', 'PathResolve']
WINDOWS_SLASH_COMPAT = True
DEFAULT_URI_SCHEMES = [
 'http', 'https', 'file', 'ftp', 'data', 'pep302']
if not hasattr(urllib2, 'HTTPSHandler'):
    DEFAULT_URI_SCHEMES.remove('https')
DEFAULT_URI_SCHEMES = tuple(DEFAULT_URI_SCHEMES)
_validationSetupCompleted = False

def _initUriValidationRegex():
    """
    Called internally to compile the regular expressions needed by
    URI validation functions, just once, the first time a function
    that needs them is called.
    """
    global URI_PATTERN
    global URI_REF_PATTERN
    global _validationSetupCompleted
    if _validationSetupCompleted:
        return
    pchar = "(?:[0-9A-Za-z\\-_\\.!~*'();:@&=+$,]|(?:%[0-9A-Fa-f]{2}))"
    fragment = "(?:[0-9A-Za-z\\-_\\.!~*'();:@&=+$,/?]|(?:%[0-9A-Fa-f]{2}))*"
    query = fragment
    segment_nz_nc = "(?:[0-9A-Za-z\\-_\\.!~*'();@&=+$,]|(?:%[0-9A-Fa-f]{2}))+"
    segment_nz = '%s+' % pchar
    segment = '%s*' % pchar
    path_rootless = '%s(?:/%s)*' % (segment_nz, segment)
    path_noscheme = '%s(?:/%s)*' % (segment_nz_nc, segment)
    path_absolute = '/(?:%s)?' % path_rootless
    path_abempty = '(?:/%s)*' % segment
    domainlabel = '[0-9A-Za-z](?:[0-9A-Za-z\\-]{0,61}[0-9A-Za-z])?'
    qualified = '(?:\\.%s)*\\.?' % domainlabel
    reg_name = "(?:(?:[0-9A-Za-z\\-_\\.!~*'();&=+$,]|(?:%[0-9A-Fa-f]{2}))*)"
    dec_octet = '(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])'
    IPv4address = '(?:%s\\.){3}(?:%s)' % (dec_octet, dec_octet)
    h16 = '[0-9A-Fa-f]{1,4}'
    ls32 = '(?:(?:%s:%s)|%s)' % (h16, h16, IPv4address)
    IPv6address = '(?:' + '(?:(?:%s:){6}%s)' % (h16, ls32) + '|(?:::(?:%s:){5}%s)' % (h16, ls32) + '|(?:%s?::(?:%s:){4}%s)' % (h16, h16, ls32) + '|(?:(?:(?:%s:)?%s)?::(?:%s:){3}%s)' % (h16, h16, h16, ls32) + '|(?:(?:(?:%s:)?%s){0,2}::(?:%s:){2}%s)' % (h16, h16, h16, ls32) + '|(?:(?:(?:%s:)?%s){0,3}::%s:%s)' % (h16, h16, h16, ls32) + '|(?:(?:(?:%s:)?%s){0,4}::%s)' % (h16, h16, ls32) + '|(?:(?:(?:%s:)?%s){0,5}::%s)' % (h16, h16, h16) + '|(?:(?:(?:%s:)?%s){0,6}::)' % (h16, h16) + ')'
    IPvFuture = "(?:v[0-9A-Fa-f]+\\.[0-9A-Za-z\\-\\._~!$&'()*+,;=:]+)"
    IP_literal = '\\[(?:%s|%s)\\]' % (IPv6address, IPvFuture)
    port = '[0-9]*'
    host = '(?:%s|%s|%s)?' % (IP_literal, IPv4address, reg_name)
    userinfo = "(?:[0-9A-Za-z\\-_\\.!~*'();:@&=+$,]|(?:%[0-9A-Fa-f]{2}))*"
    authority = '(?:%s@)?%s(?::%s)?' % (userinfo, host, port)
    scheme = '[A-Za-z][0-9A-Za-z+\\-\\.]*'
    relative_part = '(?:(?://%s%s)|(?:%s)|(?:%s))?' % (authority, path_abempty, path_absolute, path_noscheme)
    relative_ref = '%s(?:\\?%s)?(?:#%s)?' % (relative_part, query, fragment)
    hier_part = '(?:(?://%s%s)|(?:%s)|(?:%s))?' % (authority, path_abempty, path_absolute, path_rootless)
    URI = '%s:%s(?:\\?%s)?(?:#%s)?' % (scheme, hier_part, query, fragment)
    URI_reference = '(?:%s|%s)' % (URI, relative_ref)
    STRICT_URI_PYREGEX = '\\A%s\\Z' % URI
    STRICT_URIREF_PYREGEX = '\\A(?!\\n)%s\\Z' % URI_reference
    URI_PATTERN = re.compile(STRICT_URI_PYREGEX)
    URI_REF_PATTERN = re.compile(STRICT_URIREF_PYREGEX)
    _validationSetupCompleted = True
    return


def MatchesUriRefSyntax(s):
    """
    This function returns true if the given string could be a URI reference,
    as defined in RFC 3986, just based on the string's syntax.

    A URI reference can be a URI or certain portions of one, including the
    empty string, and it can have a fragment component.
    """
    if not _validationSetupCompleted:
        _initUriValidationRegex()
    return URI_REF_PATTERN.match(s) is not None
    return


def MatchesUriSyntax(s):
    """
    This function returns true if the given string could be a URI, as defined
    in RFC 3986, just based on the string's syntax.

    A URI is by definition absolute (begins with a scheme) and does not end
    with a #fragment. It also must adhere to various other syntax rules.
    """
    if not _validationSetupCompleted:
        _initUriValidationRegex()
    return URI_PATTERN.match(s) is not None
    return


_splitUriRefSetupCompleted = False

def _initSplitUriRefPattern():
    """
    Called internally to compile the regular expression used by
    SplitUriRef() just once, the first time the function is called.
    """
    global SPLIT_URI_REF_PATTERN
    global _splitUriRefSetupCompleted
    if _splitUriRefSetupCompleted:
        return
    regex = '^(?:(?P<scheme>[^:/?#]+):)?(?://(?P<authority>[^/?#]*))?(?P<path>[^?#]*)(?:\\?(?P<query>[^#]*))?(?:#(?P<fragment>.*))?$'
    SPLIT_URI_REF_PATTERN = re.compile(regex)
    _splitUriRefSetupCompleted = True
    return


def SplitUriRef(uriref):
    """
    Given a valid URI reference as a string, returns a tuple representing the
    generic URI components, as per RFC 3986 appendix B. The tuple's structure
    is (scheme, authority, path, query, fragment).

    All values will be strings (possibly empty) or None if undefined.

    Note that per RFC 3986, there is no distinction between a path and
    an "opaque part", as there was in RFC 2396.
    """
    if not _splitUriRefSetupCompleted:
        _initSplitUriRefPattern()
    g = SPLIT_URI_REF_PATTERN.match(uriref).groupdict()
    scheme = g['scheme']
    authority = g['authority']
    path = g['path']
    query = g['query']
    fragment = g['fragment']
    return (scheme, authority, path, query, fragment)


def UnsplitUriRef(uriRefSeq):
    """
    Given a sequence as would be produced by SplitUriRef(), assembles and
    returns a URI reference as a string.
    """
    if not isinstance(uriRefSeq, (tuple, list)):
        raise TypeError('sequence expected, got %s' % type(uriRefSeq))
    (scheme, authority, path, query, fragment) = uriRefSeq
    uri = ''
    if scheme is not None:
        uri += scheme + ':'
    if authority is not None:
        uri += '//' + authority
    uri += path
    if query is not None:
        uri += '?' + query
    if fragment is not None:
        uri += '#' + fragment
    return uri
    return


_splitAuthoritySetupCompleted = False

def _initSplitAuthorityPattern():
    """
    Called internally to compile the regular expression used by
    SplitAuthority() just once, the first time the function is called.
    """
    global SPLIT_AUTHORITY_PATTERN
    global _splitAuthoritySetupCompleted
    if _splitAuthoritySetupCompleted:
        return
    regex = '(?:(?P<userinfo>[^@]*)@)?(?P<host>[^:]*)(?::(?P<port>.*))?'
    SPLIT_AUTHORITY_PATTERN = re.compile(regex)
    _splitAuthoritySetupCompleted = True
    return


def SplitAuthority(authority):
    """
    Given a string representing the authority component of a URI, returns
    a tuple consisting of the subcomponents (userinfo, host, port). No
    percent-decoding is performed.
    """
    if not _splitAuthoritySetupCompleted:
        _initSplitAuthorityPattern()
    m = SPLIT_AUTHORITY_PATTERN.match(authority)
    if m:
        return m.groups()
    else:
        return (
         None, authority, None)
    return


def SplitFragment(uri):
    """
    Given a URI or URI reference, returns a tuple consisting of
    (base, fragment), where base is the portion before the '#' that
    precedes the fragment component.
    """
    pos = uri.rfind('#')
    if pos == -1:
        return (
         uri, uri[:0])
    else:
        return (
         uri[:pos], uri[pos + 1:])


UNRESERVED_PATTERN = re.compile('[0-9A-Za-z\\-\\._~]')
RESERVED = "/=&+?#;@,:$!*[]()'"
SURR_DC00 = unichr(56320)

def _chars(s):
    r"""
    This generator function helps iterate over the characters in a
    string. When the string is unicode and a surrogate pair is
    encountered, the pair is returned together, regardless of whether
    Python was built with 32-bit ('wide') or 16-bit code values for
    its internal representation of unicode. This function will raise a
    ValueError if it detects an illegal surrogate pair.

    For example, given s = u'\ud800\udc00\U00010000',
    with narrow-char unicode, "for c in s" normally iterates 4 times,
    producing u'\ud800', u'\udc00', 'u\ud800', u'\udc00', while
    "for c in _chars(s)" will iterate 2 times: producing
    u'\ud800\udc00' both times; and with wide-char unicode,
    "for c in s" iterates 3 times, producing u'\ud800', u'\udc00',
    and u'\U00010000', while "for c in _chars(s)" will iterate 2 times,
    producing u'\U00010000' both times.

    With this function, the value yielded in each iteration is thus
    guaranteed to represent a single abstract character, allowing for
    ideal encoding by the built-in codecs, as is necessary when
    percent-encoding.
    """
    if isinstance(s, str):
        for i in s:
            yield i

        return
    s = iter(s)
    for i in s:
        if '\ud7ff' < i < SURR_DC00:
            try:
                j = s.next()
            except StopIteration:
                raise ValueError('Bad pair: string ends after %r' % i)
            else:
                if SURR_DC00 <= j < '\ue000':
                    yield i + j
                else:
                    raise ValueError('Bad pair: %r (bad second half)' % (i + j))
        elif SURR_DC00 <= i < '\ue000':
            raise ValueError('Bad pair: %r (no first half)' % i)
        else:
            yield i


def PercentEncode(s, encoding='utf-8', encodeReserved=True, spaceToPlus=False, nlChars=None, reservedChars=RESERVED):
    r"""
    [*** Experimental API ***] This function applies percent-encoding, as
    described in RFC 3986 sec. 2.1, to the given string, in order to prepare
    the string for use in a URI. It replaces characters that are not allowed
    in a URI. By default, it also replaces characters in the reserved set,
    which normally includes the generic URI component delimiters ":" "/"
    "?" "#" "[" "]" "@" and the subcomponent delimiters "!" "$" "&" "'" "("
    ")" "*" "+" "," ";" "=".

    Ideally, this function should be used on individual components or
    subcomponents of a URI prior to assembly of the complete URI, not
    afterward, because this function has no way of knowing which characters
    in the reserved set are being used for their reserved purpose and which
    are part of the data. By default it assumes that they are all being used
    as data, thus they all become percent-encoded.

    The characters in the reserved set can be overridden from the default by
    setting the reservedChars argument. The percent-encoding of characters
    in the reserved set can be disabled by unsetting the encodeReserved flag.
    Do this if the string is an already-assembled URI or a URI component,
    such as a complete path.

    If the given string is Unicode, the name of the encoding given in the
    encoding argument will be used to determine the percent-encoded octets
    for characters that are not in the U+0000 to U+007F range. The codec
    identified by the encoding argument must return a byte string.

    If the given string is not Unicode, the encoding argument is ignored and
    the string is interpreted to represent literal octets, rather than
    characters. Octets above \x7F will be percent-encoded as-is, e.g., \xa0
    becomes %A0, not, say, %C2%A0.

    The spaceToPlus flag controls whether space characters are changed to
    "+" characters in the result, rather than being percent-encoded.
    Generally, this is not required, and given the status of "+" as a
    reserved character, is often undesirable. But it is required in certain
    situations, such as when generating application/x-www-form-urlencoded
    content or RFC 3151 public identifier URNs, so it is supported here.

    The nlChars argument, if given, is a sequence type in which each member
    is a substring that indicates a "new line". Occurrences of this substring
    will be replaced by '%0D%0A' in the result, as is required when generating
    application/x-www-form-urlencoded content.

    This function is similar to urllib.quote(), but is more conformant and
    Unicode-friendly. Suggestions for improvements welcome.
    """
    res = ''
    is_unicode = isinstance(s, unicode)
    if nlChars is not None:
        for c in nlChars:
            s.replace(c, '\r\n')

    for c in _chars(s):
        if is_unicode and len(c) - 1:
            for octet in c.encode(encoding):
                res += '%%%02X' % ord(octet)

        elif UNRESERVED_PATTERN.match(c) is None:
            cp = ord(c)
            if cp < 128:
                if spaceToPlus and c == ' ':
                    res += '+'
                elif c in reservedChars:
                    if encodeReserved:
                        res += '%%%02X' % cp
                    else:
                        res += c
                else:
                    res += '%%%02X' % cp
            elif is_unicode:
                for octet in c.encode(encoding):
                    res += '%%%02X' % ord(octet)

            else:
                for octet in c:
                    res += '%%%02X' % ord(octet)

        else:
            res += c

    return res
    return


def PercentDecode(s, encoding='utf-8', decodable=None):
    r"""
    [*** Experimental API ***] Reverses the percent-encoding of the given
    string.

    This function is similar to urllib.unquote(), but can also process a
    Unicode string, not just a regular byte string.

    By default, all percent-encoded sequences are decoded, but if a byte
    string is given via the 'decodable' argument, only the sequences
    corresponding to those octets will be decoded.

    If the string is Unicode, the percent-encoded sequences are converted to
    bytes, then converted back to Unicode according to the encoding given in
    the encoding argument. For example, by default, u'abc%E2%80%A2' will be
    converted to u'abc\u2022', because byte sequence E2 80 A2 represents
    character U+2022 in UTF-8.

    If the string is not Unicode, the percent-encoded octets are just
    converted to bytes, and the encoding argument is ignored. For example,
    'abc%E2%80%A2' will be converted to 'abc•'.

    This function is intended for use on the portions of a URI that are
    delimited by reserved characters (see PercentEncode), or on a value from
    data of media type application/x-www-form-urlencoded.
    """
    is_unicode = isinstance(s, unicode)
    if is_unicode:
        mychr = unichr
    else:
        mychr = chr
    list_ = s.split('%')
    res = [list_[0]]
    myappend = res.append
    del list_[0]
    for item in list_:
        if item[1:2]:
            try:
                c = mychr(int(item[:2], 16))
                if decodable is None:
                    myappend(c + item[2:])
                elif c in decodable:
                    myappend(c + item[2:])
                else:
                    myappend('%' + item)
            except ValueError:
                myappend('%' + item)

        else:
            myappend('%' + item)

    s = ('').join(res)
    if is_unicode:
        s = s.encode('iso-8859-1').decode(encoding)
    return s
    return


def Absolutize(uriRef, baseUri):
    """
    Resolves a URI reference to absolute form, effecting the result of RFC
    3986 section 5. The URI reference is considered to be relative to the
    given base URI.

    It is the caller's responsibility to ensure that the base URI matches
    the absolute-URI syntax rule of RFC 3986, and that its path component
    does not contain '.' or '..' segments if the scheme is hierarchical.
    Unexpected results may occur otherwise.

    This function only conducts a minimal sanity check in order to determine
    if relative resolution is possible: it raises a UriException if the base
    URI does not have a scheme component. While it is true that the base URI
    is irrelevant if the URI reference has a scheme, an exception is raised
    in order to signal that the given string does not even come close to
    meeting the criteria to be usable as a base URI.

    It is the caller's responsibility to make a determination of whether the
    URI reference constitutes a "same-document reference", as defined in RFC
    2396 or RFC 3986. As per the spec, dereferencing a same-document
    reference "should not" involve retrieval of a new representation of the
    referenced resource. Note that the two specs have different definitions
    of same-document reference: RFC 2396 says it is *only* the cases where the
    reference is the empty string, or "#" followed by a fragment; RFC 3986
    requires making a comparison of the base URI to the absolute form of the
    reference (as is returned by the spec), minus its fragment component,
    if any.

    This function is similar to urlparse.urljoin() and urllib.basejoin().
    Those functions, however, are (as of Python 2.3) outdated, buggy, and/or
    designed to produce results acceptable for use with other core Python
    libraries, rather than being earnest implementations of the relevant
    specs. Their problems are most noticeable in their handling of
    same-document references and 'file:' URIs, both being situations that
    come up far too often to consider the functions reliable enough for
    general use.
    """
    if not baseUri or not IsAbsolute(baseUri):
        raise UriException(UriException.RELATIVE_BASE_URI, base=baseUri, ref=uriRef)
    if uriRef == '' or uriRef[0] == '#':
        return baseUri.split('#')[0] + uriRef
    tScheme = tAuth = tPath = tQuery = None
    (rScheme, rAuth, rPath, rQuery, rFrag) = SplitUriRef(uriRef)
    if rScheme is not None:
        tScheme = rScheme
        tAuth = rAuth
        tPath = RemoveDotSegments(rPath)
        tQuery = rQuery
    else:
        (bScheme, bAuth, bPath, bQuery, bFrag) = SplitUriRef(baseUri)
        if rAuth is not None:
            tAuth = rAuth
            tPath = RemoveDotSegments(rPath)
            tQuery = rQuery
        else:
            if not rPath:
                tPath = bPath
                tQuery = rQuery is not None and rQuery or bQuery
            else:
                if rPath[0] == '/':
                    tPath = RemoveDotSegments(rPath)
                else:
                    if bAuth is not None and not bPath:
                        tPath = '/' + rPath
                    else:
                        tPath = bPath[:bPath.rfind('/') + 1] + rPath
                    tPath = RemoveDotSegments(tPath)
                tQuery = rQuery
            tAuth = bAuth
        tScheme = bScheme
    return UnsplitUriRef((tScheme, tAuth, tPath, tQuery, rFrag))
    return


def Relativize(targetUri, againstUri, subPathOnly=False):
    """
    This method returns a relative URI that is consistent with `targetURI`
    when resolved against `againstUri`.  If no such relative URI exists, for
    whatever reason, this method returns `None`.

    To be precise, if a string called `rel` exists such that
    ``Absolutize(rel, againstUri) == targetUri``, then `rel` is returned by
    this function.  In these cases, `Relativize` is in a sense the inverse
    of `Absolutize`.  In all other cases, `Relativize` returns `None`.

    The following idiom may be useful for obtaining compliant relative
    reference strings (e.g. for `path`) for use in other methods of this
    package::

      path = Relativize(OsPathToUri(path), OsPathToUri('.'))

    If `subPathOnly` is `True`, then this method will only return a relative
    reference if such a reference exists relative to the last hierarchical
    segment of `againstUri`.  In particular, this relative reference will
    not start with '/' or '../'.
    """
    if not IsAbsolute(targetUri) or not IsAbsolute(againstUri):
        return None
    targetUri = NormalizePathSegmentsInUri(targetUri)
    againstUri = NormalizePathSegmentsInUri(againstUri)
    splitTarget = list(SplitUriRef(Absolutize(targetUri, targetUri)))
    splitAgainst = list(SplitUriRef(Absolutize(againstUri, againstUri)))
    if not splitTarget[:2] == splitAgainst[:2]:
        return None
    subPathSplit = [None, None] + splitTarget[2:]
    targetPath = splitTarget[2]
    againstPath = splitAgainst[2]
    leadingSlash = False
    if targetPath[:1] == '/' or againstPath[:1] == '/':
        if targetPath[:1] == againstPath[:1]:
            targetPath = targetPath[1:]
            againstPath = againstPath[1:]
            leadingSlash = True
        else:
            return None
    targetPathSegments = targetPath.split('/')
    againstPathSegments = againstPath.split('/')
    i = 0
    while True:
        if not (len(targetPathSegments) > i and len(againstPathSegments) > i):
            break
        if targetPathSegments[i] == againstPathSegments[i] and not (i + 1 == len(againstPathSegments) and '' == againstPathSegments[i]) and not (i + 1 == len(targetPathSegments) and '' == targetPathSegments[i]):
            i = i + 1
        else:
            break

    traverse = len(againstPathSegments) - i - 1
    relativePath = None
    if i == 0 and leadingSlash:
        if len(againstPathSegments) == 1:
            relativePath = targetPath
        elif subPathOnly:
            return None
        else:
            relativePath = '/' + targetPath
    elif traverse > 0:
        if subPathOnly:
            return None
        relativePath = '../' * traverse + ('/').join(targetPathSegments[i:])
    elif len(targetPathSegments) > i + 1 and '' == targetPathSegments[i]:
        relativePath = './' + ('/').join(targetPathSegments[i:])
    else:
        relativePath = ('/').join(targetPathSegments[i:])
    return UnsplitUriRef([None, None, relativePath] + splitTarget[3:])
    return


def RemoveDotSegments(path):
    """
    Supports Absolutize() by implementing the remove_dot_segments function
    described in RFC 3986 sec. 5.2.  It collapses most of the '.' and '..'
    segments out of a path without eliminating empty segments. It is intended
    to be used during the path merging process and may not give expected
    results when used independently. Use NormalizePathSegments() or
    NormalizePathSegmentsInUri() if more general normalization is desired.
    """
    if path == '.' or path == '..':
        return path[0:0]
    while path:
        if path[:2] == './':
            path = path[2:]
        elif path[:3] == '../':
            path = path[3:]
        else:
            break

    leading_slash = False
    if path[:1] == '/':
        path = path[1:]
        leading_slash = True
    if path[-2:] == '/.':
        path = path[:-1]
    segments = path.split('/')
    keepers = []
    segments.reverse()
    while segments:
        seg = segments.pop()
        if seg == '..':
            if keepers:
                keepers.pop()
            elif not leading_slash:
                keepers.append(seg)
            if not segments:
                keepers.append('')
        elif seg != '.':
            keepers.append(seg)

    return leading_slash * '/' + ('/').join(keepers)


def NormalizeCase(uriRef, doHost=False):
    """
    Returns the given URI reference with the case of the scheme,
    percent-encoded octets, and, optionally, the host, all normalized,
    implementing section 6.2.2.1 of RFC 3986. The normal form of
    scheme and host is lowercase, and the normal form of
    percent-encoded octets is uppercase.

    The URI reference can be given as either a string or as a sequence as
    would be provided by the SplitUriRef function. The return value will
    be a string or tuple.
    """
    if not isinstance(uriRef, (tuple, list)):
        uriRef = SplitUriRef(uriRef)
        tup = None
    else:
        tup = True
    newRef = []
    for component in uriRef:
        if component:
            newRef.append(re.sub('%([0-9a-f][0-9a-f])', lambda m: m.group(0).upper(), component))
        else:
            newRef.append(component)

    scheme = newRef[0]
    if scheme:
        scheme = scheme.lower()
    authority = newRef[1]
    if doHost:
        if authority:
            (userinfo, host, port) = SplitAuthority(authority)
            authority = ''
            if userinfo is not None:
                authority += '%s@' % userinfo
            authority += host.lower()
            if port is not None:
                authority += ':%s' % port
    res = (
     scheme, authority, newRef[2], newRef[3], newRef[4])
    if tup:
        return res
    else:
        return UnsplitUriRef(res)
    return


def NormalizePercentEncoding(s):
    """
    Given a string representing a URI reference or a component thereof,
    returns the string with all percent-encoded octets that correspond to
    unreserved characters decoded, implementing section 6.2.2.2 of RFC
    3986.
    """
    return PercentDecode(s, decodable='0123456789%s-._~' % ascii_letters)


def NormalizePathSegments(path):
    """
    Given a string representing the path component of a URI reference having a
    hierarchical scheme, returns the string with dot segments ('.' and '..')
    removed, implementing section 6.2.2.3 of RFC 3986. If the path is
    relative, it is returned with no changes.
    """
    if not path or path[:1] != '/':
        return path
    else:
        return RemoveDotSegments(path)


def NormalizePathSegmentsInUri(uri):
    """
    Given a string representing a URI or URI reference having a hierarchical
    scheme, returns the string with dot segments ('.' and '..') removed from
    the path component, implementing section 6.2.2.3 of RFC 3986. If the
    path is relative, the URI or URI reference is returned with no changes.
    """
    components = list(SplitUriRef(uri))
    components[2] = NormalizePathSegments(components[2])
    return UnsplitUriRef(components)


class UriResolverBase:
    __module__ = __name__
    '\n    This is class provides a set of functions related to the resolution of\n    URIs, including the resolution to absolute form of URI references, and\n    the retrieval of a representation of a resource that is identified by a\n    URI.\n\n    The object attribute supportedSchemes is a list of URI schemes supported\n    for dereferencing (representation retrieval). Schemes supported by\n    default are: %s.\n    ' % (', ').join(DEFAULT_URI_SCHEMES)

    def __init__(self):
        self.supportedSchemes = list(DEFAULT_URI_SCHEMES)

    def normalize(self, uriRef, baseUri):
        """
        Resolves a URI reference to absolute form, effecting the result of RFC
        3986 section 5. The URI reference is considered to be relative to
        the given base URI.

        Also verifies that the resulting URI reference has a scheme that
        resolve() supports, raising a UriException if it doesn't.

        The default implementation does not perform any validation on the base
        URI beyond that performed by Absolutize().
        """
        scheme = GetScheme(uriRef) or GetScheme(baseUri)
        if scheme in self.supportedSchemes:
            return Absolutize(uriRef, baseUri)
        elif scheme is None:
            raise ValueError('When the URI to resolve is a relative reference, it must be accompanied by a base URI.')
        else:
            raise UriException(UriException.UNSUPPORTED_SCHEME, scheme=scheme, resolver=self.__class__.__name__)
        return

    def resolve(self, uri, baseUri=None):
        """
        This function takes a URI or a URI reference plus a base URI, produces
        a normalized URI using the normalize function if a base URI was given,
        then attempts to obtain access to an entity representing the resource
        identified by the resulting URI, returning the entity as a stream (a
        Python file-like object).

        Raises a UriException if the URI scheme is unsupported or if a stream
        could not be obtained for any reason.
        """
        if baseUri is not None:
            uri = self.normalize(uri, baseUri)
            scheme = GetScheme(uri)
        else:
            scheme = GetScheme(uri)
            if scheme not in self.supportedSchemes:
                if scheme is None:
                    raise ValueError('When the URI to resolve is a relative reference, it must be accompanied by a base URI.')
                else:
                    raise UriException(UriException.UNSUPPORTED_SCHEME, scheme=scheme, resolver=self.__class__.__name__)
        if scheme == 'file':
            path = UriToOsPath(uri, attemptAbsolute=False)
            try:
                stream = open(path, 'rb')
            except IOError, e:
                raise UriException(UriException.RESOURCE_ERROR, loc='%s (%s)' % (uri, path), uri=uri, msg=str(e))

        else:
            try:
                stream = UrlOpen(uri)
            except IOError, e:
                raise UriException(UriException.RESOURCE_ERROR, uri=uri, loc=uri, msg=str(e))

        return stream
        return

    def generate(self, hint=None):
        """
        This function generates and returns a URI.
        The hint is an object that helps decide what to generate.
        The default action is to generate a random UUID URN.
        """
        import Uuid
        return 'urn:uuid:' + Uuid.UuidAsString(Uuid.GenerateUuid())


class FtUriResolver(UriResolverBase):
    """
    The URI resolver class used by most of 4Suite, outside of the repository.

    Adds support for lenient processing of base URIs.
    """
    __module__ = __name__

    def normalize(self, uriRef, baseUri):
        """
        This function differs from UriResolverBase.normalize() in the
        following manner:

        This function allows for the possibility of the base URI beginning
        with a '/', in which case the argument is assumed to be an absolute
        path component of 'file' URI that has no authority component.
        """
        if baseUri[:1] == '/':
            baseUri = 'file://' + baseUri
        return UriResolverBase.normalize(self, uriRef, baseUri)


BASIC_RESOLVER = FtUriResolver()
_urlopener = None

class _DataHandler(urllib2.BaseHandler):
    """
    A class to handle 'data' URLs.

    The actual handling is done by urllib.URLopener.open_data() method.
    """
    __module__ = __name__

    def data_open(self, request):
        global _urlopener
        if _urlopener is None:
            _urlopener = urllib.URLopener()
        return _urlopener.open_data(self, request.get_full_url())
        return


def ResourceToUri(package, resource):
    """Return a PEP 302 pseudo-URL for the specified resource.

    'package' is a Python module name (dot-separated module names) and
    'resource' is a '/'-separated pathname.
    """
    (provider, resource_name) = ImportUtil.NormalizeResource(package, resource)
    if provider.loader:
        segments = resource_name.split('/')
        if not resource.startswith('/'):
            dirname = provider.module_path[len(provider.zip_pre):]
            segments[0:0] = dirname.split(os.sep)
        path = ('/').join(map(PercentEncode, segments))
        uri = 'pep302://%s/%s' % (package, path)
    else:
        filename = ImportUtil.GetResourceFilename(package, resource)
        uri = OsPathToUri(filename)
    return uri


class _Pep302Handler(urllib2.FileHandler):
    """
    A class to handler opening of PEP 302 pseudo-URLs.

    The syntax for this pseudo-URL is:
        url    := "pep302://" module "/" path
        module := <Python module name>
        path   := <'/'-separated pathname>

    The "path" portion of the URL will be passed to the get_data() method
    of the loader identified by "module" with '/'s converted to the OS
    native path separator.
    """
    __module__ = __name__

    def pep302_open(self, request):
        import mimetypes, mimetools, rfc822
        package = request.get_host()
        resource = request.get_selector()
        resource = PercentDecode(re.sub('%2[fF]', '\\/', resource))
        try:
            stream = ImportUtil.GetResourceStream(package, resource)
        except EnvironmentError, error:
            raise urllib2.URLError(str(error))

        try:
            stream.seek(0, 2)
        except IOError:
            data = stream.read()
            stream = cStringIO.StringIO(data)
            length = len(data)
        else:
            length = stream.tell()
            stream.seek(0, 0)

        mtime = ImportUtil.GetResourceLastModified(package, resource)
        mtime = rfc822.formatdate(mtime)
        mtype = mimetypes.guess_type(resource) or 'text/plain'
        headers = 'Content-Type: %s\nContent-Length: %d\nLast-Modified: %s\n' % (mtype, length, mtime)
        headers = mimetools.Message(cStringIO.StringIO(headers))
        return urllib.addinfourl(stream, headers, request.get_full_url())


_opener = None

def UrlOpen(url, *args, **kwargs):
    """
    A replacement/wrapper for urllib2.urlopen().

    Simply calls MakeUrllibSafe() on the given URL and passes the result
    and all other args to urllib2.urlopen().
    """
    global _opener
    if _opener is None:
        _opener = urllib2.build_opener(_DataHandler, _Pep302Handler)
    stream = _opener.open(MakeUrllibSafe(url), *args, **kwargs)
    stream.name = url
    return stream
    return


def UrnToPublicId(urn):
    """
    Converts a URN that conforms to RFC 3151 to a public identifier.

    For example, the URN
    "urn:publicid:%2B:IDN+example.org:DTD+XML+Bookmarks+1.0:EN:XML"
    will be converted to the public identifier
    "+//IDN example.org//DTD XML Bookmarks 1.0//EN//XML"

    Raises a UriException if the given URN cannot be converted.
    Query and fragment components, if present, are ignored.
    """
    if urn is not None and urn:
        (scheme, auth, path, query, frag) = SplitUriRef(urn)
        if scheme is not None and scheme.lower() == 'urn':
            pp = path.split(':', 1)
            if len(pp) > 1:
                urn_scheme = PercentDecode(pp[0])
                if urn_scheme == 'publicid':
                    publicid = pp[1].replace('+', ' ')
                    publicid = publicid.replace(':', '//')
                    publicid = publicid.replace(';', '::')
                    publicid = PercentDecode(publicid)
                    return publicid
    raise UriException(UriException.INVALID_PUBLIC_ID_URN, urn=urn)
    return


def PublicIdToUrn(publicid):
    """
    Converts a public identifier to a URN that conforms to RFC 3151.
    """
    publicid = re.sub('[ \t\r\n]+', ' ', publicid.strip())
    r = (':').join([ (';').join([ PercentEncode(dcpart, spaceToPlus=True) for dcpart in dspart.split('::') ]) for dspart in publicid.split('//') ])
    return 'urn:publicid:%s' % r


SCHEME_PATTERN = re.compile('([a-zA-Z][a-zA-Z0-9+\\-.]*):')

def GetScheme(uriRef):
    """
    Obtains, with optimum efficiency, just the scheme from a URI reference.
    Returns a string, or if no scheme could be found, returns None.
    """
    m = SCHEME_PATTERN.match(uriRef)
    if m is None:
        return None
    else:
        return m.group(1)
    return


def StripFragment(uriRef):
    """
    Returns the given URI or URI reference with the fragment component, if
    any, removed.
    """
    return SplitFragment(uriRef)[0]


def IsAbsolute(identifier):
    """
    Given a string believed to be a URI or URI reference, tests that it is
    absolute (as per RFC 3986), not relative -- i.e., that it has a scheme.
    """
    return GetScheme(identifier) is not None
    return


_ntPathToUriSetupCompleted = False

def _initNtPathPattern():
    """
    Called internally to compile the regular expression used by
    OsPathToUri() on Windows just once, the first time the function is
    called.
    """
    global NT_PATH_PATTERN
    global _ntPathToUriSetupCompleted
    if _ntPathToUriSetupCompleted:
        return
    drive = '(?P<drive>[A-Za-z])'
    host = '(?P<host>[^\\\\]*)'
    share = '(?P<share>[^\\\\]+)'
    abs_path = '(?P<abspath>\\\\(?:[^\\\\]+\\\\?)*)'
    rel_path = '(?P<relpath>(?:[^\\\\]+\\\\?)*)'
    NT_PATH_REGEX = '^(?:%s:)?(?:(?:(?:\\\\\\\\%s\\\\%s)?%s)|%s)$' % (drive, host, share, abs_path, rel_path)
    NT_PATH_PATTERN = re.compile(NT_PATH_REGEX)
    _ntPathToUriSetupCompleted = True
    return


def _splitNtPath(path):
    """
    Called internally to get a tuple representing components of the given
    Windows path.
    """
    if not _ntPathToUriSetupCompleted:
        _initNtPathPattern()
    m = NT_PATH_PATTERN.match(path)
    if not m:
        raise ValueError('Path %s is not a valid Windows path.')
    components = m.groupdict()
    (drive, host, share, abspath, relpath) = (components['drive'], components['host'], components['share'], components['abspath'], components['relpath'])
    return (
     drive, host, share, abspath, relpath)


def _getDriveLetter(s):
    """
    Called internally to get a drive letter from a string, if the string
    is a drivespec.
    """
    if len(s) == 2 and s[1] in ':|' and s[0] in ascii_letters:
        return s[0]
    return


def OsPathToUri(path, attemptAbsolute=True, osname=None):
    r"""This function converts an OS-specific file system path to a URI of
    the form 'file:///path/to/the/file'.

    In addition, if the path is absolute, any dot segments ('.' or '..') will
    be collapsed, so that the resulting URI can be safely used as a base URI
    by functions such as Absolutize().

    The given path will be interpreted as being one that is appropriate for
    use on the local operating system, unless a different osname argument is
    given.

    If the given path is relative, an attempt may be made to first convert
    the path to absolute form by interpreting the path as being relative
    to the current working directory.  This is the case if the attemptAbsolute
    flag is True (the default).  If attemptAbsolute is False, a relative
    path will result in a URI of the form file:relative/path/to/a/file .

    attemptAbsolute has no effect if the given path is not for the
    local operating system.

    On Windows, the drivespec will become the first step in the path component
    of the URI. If the given path contains a UNC hostname, this name will be
    used for the authority component of the URI.

    Warning: Some libraries, such as urllib.urlopen(), may not behave as
    expected when given a URI generated by this function. On Windows you may
    want to call re.sub('(/[A-Za-z]):', r'\1|', uri) on the URI to prepare it
    for use by functions such as urllib.url2pathname() or urllib.urlopen().

    This function is similar to urllib.pathname2url(), but is more featureful
    and produces better URIs.
    """
    osname = osname or os.name
    if osname == 'nt':
        if WINDOWS_SLASH_COMPAT:
            path = path.replace('/', '\\')
        (drive, host, share, abspath, relpath) = _splitNtPath(path)
        if attemptAbsolute and relpath is not None and osname == os.name:
            path = os.path.join(os.getcwd(), relpath)
            (drive, host, share, abspath, relpath) = _splitNtPath(path)
        path = abspath or relpath
        path = ('/').join([ PercentEncode(seg) for seg in path.split('\\') ])
        uri = 'file:'
        if host:
            uri += '//%s' % PercentEncode(host)
        elif abspath:
            uri += '//'
        if drive:
            uri += '/%s:' % drive.upper()
        if share:
            uri += '/%s' % PercentEncode(share)
        if abspath:
            path = RemoveDotSegments(path)
        uri += path
    elif osname == 'posix':
        try:
            from posixpath import isabs
        except ImportError:
            isabs = lambda p: p[:1] == '/'
        else:
            pathisabs = isabs(path)
            if pathisabs:
                path = RemoveDotSegments(path)
            elif attemptAbsolute and osname == os.name:
                path = os.path.join(os.getcwd(), path)
                pathisabs = isabs(path)
            path = ('/').join([ PercentEncode(seg) for seg in path.split('/') ])
            if pathisabs:
                uri = 'file://%s' % path
            else:
                uri = 'file:%s' % path
    elif osname == os.name:
        from urllib import pathname2url
        if attemptAbsolute and not os.path.isabs(path):
            path = os.path.join(os.getcwd(), path)
    else:
        try:
            module = '%surl2path' % osname
            exec 'from %s import pathname2url' % module
        except ImportError:
            raise UriException(UriException.UNSUPPORTED_PLATFORM, osname, OsPathToUri)

        uri = 'file:' + pathname2url(path)
    return uri
    return


def UriToOsPath(uri, attemptAbsolute=True, encoding='utf-8', osname=None):
    r"""
    This function converts a URI reference to an OS-specific file system path.

    If the URI reference is given as a Unicode string, then the encoding
    argument determines how percent-encoded components are interpreted, and
    the result will be a Unicode string. If the URI reference is a regular
    byte string, the encoding argument is ignored and the result will be a
    byte string in which percent-encoded octets have been converted to the
    bytes they represent. For example, the trailing path segment of
    u'file:///a/b/%E2%80%A2' will by default be converted to u'\u2022',
    because sequence E2 80 A2 represents character U+2022 in UTF-8. If the
    string were not Unicode, the trailing segment would become the 3-byte
    string '\xe2\x80\xa2'.

    The osname argument determines for what operating system the resulting
    path is appropriate. It defaults to os.name and is typically the value
    'posix' on Unix systems (including Mac OS X and Cygwin), and 'nt' on
    Windows NT/2000/XP.

    This function is similar to urllib.url2pathname(), but is more featureful
    and produces better paths.

    If the given URI reference is not relative, its scheme component must be
    'file', and an exception will be raised if it isn't.

    In accordance with RFC 3986, RFC 1738 and RFC 1630, an authority
    component that is the string 'localhost' will be treated the same as an
    empty authority.

    Dot segments ('.' or '..') in the path component are NOT collapsed.

    If the path component of the URI reference is relative and the
    attemptAbsolute flag is True (the default), then the resulting path
    will be made absolute by considering the path to be relative to the
    current working directory. There is no guarantee that such a result
    will be an accurate interpretation of the URI reference.

    attemptAbsolute has no effect if the
    result is not being produced for the local operating system.

    Fragment and query components of the URI reference are ignored.

    If osname is 'posix', the authority component must be empty or just
    'localhost'. An exception will be raised otherwise, because there is no
    standard way of interpreting other authorities. Also, if '%2F' is in a
    path segment, it will be converted to r'\/' (a backslash-escaped forward
    slash). The caller may need to take additional steps to prevent this from
    being interpreted as if it were a path segment separator.

    If osname is 'nt', a drivespec is recognized as the first occurrence of a
    single letter (A-Z, case-insensitive) followed by '|' or ':', occurring as
    either the first segment of the path component, or (incorrectly) as the
    entire authority component. A UNC hostname is recognized as a non-empty,
    non-'localhost' authority component that has not been recognized as a
    drivespec, or as the second path segment if the first path segment is
    empty. If a UNC hostname is detected, the result will begin with
    '\\<hostname>\'. If a drivespec was detected also, the first path segment
    will be '$<driveletter>$'. If a drivespec was detected but a UNC hostname
    was not, then the result will begin with '<driveletter>:'.

    Windows examples:
    'file:x/y/z' => r'x\y\z';
    'file:/x/y/z' (not recommended) => r'\x\y\z';
    'file:///x/y/z' => r'\x\y\z';
    'file:///c:/x/y/z' => r'C:\x\y\z';
    'file:///c|/x/y/z' => r'C:\x\y\z';
    'file:///c:/x:/y/z' => r'C:\x:\y\z' (bad path, valid interpretation);
    'file://c:/x/y/z' (not recommended) => r'C:\x\y\z';
    'file://host/share/x/y/z' => r'\\host\share\x\y\z';
    'file:////host/share/x/y/z' => r'\\host\share\x\y\z'
    'file://host/x:/y/z' => r'\\host\x:\y\z' (bad path, valid interp.);
    'file://localhost/x/y/z' => r'\x\y\z';
    'file://localhost/c:/x/y/z' => r'C:\x\y\z';
    'file:///C:%5Cx%5Cy%5Cz' (not recommended) => r'C:\x\y\z'
    """
    (scheme, authority, path) = SplitUriRef(uri)[0:3]
    if scheme and scheme != 'file':
        raise UriException(UriException.NON_FILE_URI, uri)
    if authority == 'localhost':
        authority = None
    osname = osname or os.name
    if osname == 'nt':
        unchost = None
        driveletter = None
        if authority:
            authority = PercentDecode(authority, encoding=encoding)
            if _getDriveLetter(authority):
                driveletter = authority[0]
            else:
                unchost = authority
        if not (driveletter or unchost):
            if WINDOWS_SLASH_COMPAT:
                regex = '%2[fF]|%5[cC]'
            else:
                regex = '%5[cC]'
            path = re.sub(regex, '/', path)
            segs = path.split('/')
            if not segs[0]:
                if len(segs) > 2 and not segs[1]:
                    unchost = PercentDecode(segs[2], encoding=encoding)
                    path = len(segs) > 3 and '/' + ('/').join(segs[3:]) or ''
                elif len(segs) > 1:
                    driveletter = _getDriveLetter(PercentDecode(segs[1], encoding=encoding))
                    if driveletter:
                        path = len(segs) > 2 and '/' + ('/').join(segs[2:]) or ''
            else:
                driveletter = _getDriveLetter(PercentDecode(segs[0], encoding=encoding))
                if driveletter:
                    path = len(segs) > 1 and path[2:] or ''
        sep = '\\'
        path = PercentDecode(path.replace('/', sep), encoding=encoding)
        if unchost:
            path = '%s%s%s' % (sep * 2, unchost, path)
        elif driveletter:
            path = '%s:%s' % (driveletter.upper(), path)
        elif path[:1] == '\\':
            path = re.sub('^\\\\+', '\\\\', path)
        elif attemptAbsolute and osname == os.name:
            path = os.path.join(os.getcwd(), path)
        return path
    if osname == 'posix':
        if authority:
            raise UriException(UriException.UNIX_REMOTE_HOST_FILE_URI, uri)
        path = PercentDecode(re.sub('%2[fF]', '\\/', path), encoding=encoding)
        if attemptAbsolute and osname == os.name and not os.path.isabs(path):
            path = os.path.join(os.getcwd(), path)
        return path
    elif osname == os.name:
        from urllib import url2pathname
    else:
        try:
            module = '%surl2path' % osname
            exec 'from %s import url2pathname' % module
        except ImportError:
            raise UriException(UriException.UNSUPPORTED_PLATFORM, osname, UriToOsPath)

        if scheme:
            uri = uri[len(scheme) + 1:]
        return url2pathname(uri)
    return


REG_NAME_HOST_PATTERN = re.compile("^(?:(?:[0-9A-Za-z\\-_\\.!~*'();&=+$,]|(?:%[0-9A-Fa-f]{2}))*)$")

def MakeUrllibSafe(uriRef):
    """
    Makes the given RFC 3986-conformant URI reference safe for passing
    to legacy urllib functions. The result may not be a valid URI.

    As of Python 2.3.3, urllib.urlopen() does not fully support
    internationalized domain names, it does not strip fragment components,
    and on Windows, it expects file URIs to use '|' instead of ':' in the
    path component corresponding to the drivespec. It also relies on
    urllib.unquote(), which mishandles unicode arguments. This function
    produces a URI reference that will work around these issues, although
    the IDN workaround is limited to Python 2.3 only. May raise a
    UnicodeEncodeError if the URI reference is Unicode and erroneously
    contains non-ASCII characters.
    """
    (scheme, auth, path, query, frag) = SplitUriRef(uriRef)
    if auth and auth.find('@') > -1:
        (userinfo, hostport) = auth.split('@')
    else:
        userinfo = None
        hostport = auth
    if hostport and hostport.find(':') > -1:
        (host, port) = hostport.split(':')
    else:
        host = hostport
        port = None
    if host and REG_NAME_HOST_PATTERN.match(host):
        host = PercentDecode(host)
        if sys.version_info[0:2] >= (2, 3):
            if isinstance(host, str):
                host = host.decode('utf-8')
            host = host.encode('idna')
        auth = ''
        if userinfo:
            auth += userinfo + '@'
        auth += host
        if port:
            auth += ':' + port
    if os.name == 'nt' and scheme == 'file':
        path = path.replace(':', '|', 1)
    uri = UnsplitUriRef((scheme, auth, path, query, None))
    if isinstance(uri, unicode):
        try:
            uri = uri.encode('us-ascii')
        except UnicodeError:
            raise UriException(Error.IDNA_UNSUPPORTED, uri=uriRef)

    return uri
    return


def PathResolve(paths):
    """
    This function takes a list of file URIs.  The first can be
    absolute or relative to the URI equivalent of the current working
    directory. The rest must be relative to the first.
    The function converts them all to OS paths appropriate for the local
    system, and then creates a single final path by resolving each path
    in the list against the following one. This final path is returned
    as a URI.
    """
    if not paths:
        return paths
    paths = [ UriToOsPath(p, attemptAbsolute=False) for p in paths ]
    if not os.path.isabs(paths[0]):
        paths[0] = os.path.join(os.getcwd(), paths[0])
    resolved = reduce(lambda a, b: BaseJoin(os.path.isdir(a) and OsPathToUri(os.path.join(a, ''), attemptAbsolute=False) or OsPathToUri(a, attemptAbsolute=False), OsPathToUri(b, attemptAbsolute=False)[5:]), paths)
    return resolved


def BaseJoin(base, uriRef):
    """
    Merges a base URI reference with another URI reference, returning a
    new URI reference.

    It behaves exactly the same as Absolutize(), except the arguments
    are reversed, and it accepts any URI reference (even a relative URI)
    as the base URI. If the base has no scheme component, it is
    evaluated as if it did, and then the scheme component of the result
    is removed from the result, unless the uriRef had a scheme. Thus, if
    neither argument has a scheme component, the result won't have one.

    This function is named BaseJoin because it is very much like
    urllib.basejoin(), but it follows the current RFC 3986 algorithms
    for path merging, dot segment elimination, and inheritance of query
    and fragment components.

    WARNING: This function exists for 2 reasons: (1) because of a need
    within the 4Suite repository to perform URI reference absolutization
    using base URIs that are stored (inappropriately) as absolute paths
    in the subjects of statements in the RDF model, and (2) because of
    a similar need to interpret relative repo paths in a 4Suite product
    setup.xml file as being relative to a path that can be set outside
    the document. When these needs go away, this function probably will,
    too, so it is not advisable to use it.
    """
    if IsAbsolute(base):
        return Absolutize(uriRef, base)
    else:
        dummyscheme = 'basejoin'
        res = Absolutize(uriRef, '%s:%s' % (dummyscheme, base))
        if IsAbsolute(uriRef):
            return res
        else:
            return res[len(dummyscheme) + 1:]


class UriDict(dict):
    """
    A dictionary that uses URIs as keys. It attempts to observe some degree of
    URI equivalence as defined in RFC 3986 section 6. For example, if URIs
    A and B are equivalent, a dictionary operation involving key B will return
    the same result as one involving key A, and vice-versa.

    This is useful in situations where retrieval of a new representation of a
    resource is undesirable for equivalent URIs, such as "file:///x" and
    "file://localhost/x" (see RFC 1738), or "http://spam/~x/",
    "http://spam/%7Ex/" and "http://spam/%7ex" (see RFC 3986).

    Normalization performed includes case normalization on the scheme and
    percent-encoded octets, percent-encoding normalization (decoding of
    octets corresponding to unreserved characters), and the reduction of
    'file://localhost/' to 'file:///', in accordance with both RFC 1738 and
    RFC 3986 (although RFC 3986 encourages using 'localhost' and doing
    this for all schemes, not just file).

    An instance of this class is used by Ft.Xml.Xslt.XsltContext for caching
    documents, so that the XSLT function document() will return identical
    nodes, without refetching/reparsing, for equivalent URIs.
    """
    __module__ = __name__

    def _normalizekey(self, key):
        key = NormalizeCase(NormalizePercentEncoding(key))
        if key[:17] == 'file://localhost/':
            return 'file://' + key[16:]
        else:
            return key

    def __getitem__(self, key):
        return super(UriDict, self).__getitem__(self._normalizekey(key))

    def __setitem__(self, key, value):
        return super(UriDict, self).__setitem__(self._normalizekey(key), value)

    def __delitem__(self, key):
        return super(UriDict, self).__delitem__(self._normalizekey(key))

    def has_key(self, key):
        return super(UriDict, self).has_key(self._normalizekey(key))

    def __contains__(self, key):
        return super(UriDict, self).__contains__(self._normalizekey(key))

    def __iter__(self):
        return iter(self.keys())

    iterkeys = __iter__

    def iteritems(self):
        for key in self.iterkeys():
            yield (
             key, self.__getitem__(key))


def FileUrl(filepath):
    import warnings
    warnings.warn('FileUrl() deprecated; use OsPathToUri()', DeprecationWarning, 2)
    return OsPathToUri(filepath, attemptAbsolute=True)