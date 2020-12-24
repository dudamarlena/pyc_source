# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/n3p/uripath.py
# Compiled at: 2008-04-06 11:56:08
"""
Uniform Resource Identifier (URI) path manipulation,
above the access layer

The name of this module and the functions are somewhat
arbitrary; they hark to other parts of the python
library; e.g. uripath.join() is somewhat like os.path.join().

REFERENCES

  Uniform Resource Identifiers (URI): Generic Syntax
  http://www.ietf.org/rfc/rfc2396.txt

  The Web Model: Information hiding and URI syntax (Jan 98)
  http://www.w3.org/DesignIssues/Model.html

  URI API design [was: URI Test Suite] Dan Connolly (Sun, Aug 12 2001)
  http://lists.w3.org/Archives/Public/uri/2001Aug/0021.html

"""
__version__ = '$Id: uripath.py,v 1.16 2004/03/21 04:24:35 timbl Exp $'
from string import find, rfind, index

def splitFrag(uriref):
    """split a URI reference between the fragment and the rest.

    Punctuation is thrown away.

    e.g.

    >>> splitFrag("abc#def")
    ('abc', 'def')

    >>> splitFrag("abcdef")
    ('abcdef', None)

    """
    i = rfind(uriref, '#')
    if i >= 0:
        return (uriref[:i], uriref[i + 1:])
    else:
        return (
         uriref, None)
    return


def splitFragP(uriref, punct=0):
    """split a URI reference before the fragment

    Punctuation is kept.

    e.g.

    >>> splitFragP("abc#def")
    ('abc', '#def')

    >>> splitFragP("abcdef")
    ('abcdef', '')

    """
    i = rfind(uriref, '#')
    if i >= 0:
        return (uriref[:i], uriref[i:])
    else:
        return (
         uriref, '')


def join(here, there):
    r"""join an absolute URI and URI reference
    (non-ascii characters are supported/doctested;
    haven't checked the details of the IRI spec though)

    here is assumed to be absolute.
    there is URI reference.

    >>> join('http://example/x/y/z', '../abc')
    'http://example/x/abc'

    Raise ValueError if there uses relative path
    syntax but here has no hierarchical path.

    >>> join('mid:foo@example', '../foo')
    Traceback (most recent call last):
        raise ValueError, here
    ValueError: Base <mid:foo@example> has no slash after colon - with relative '../foo'.

    We grok IRIs

    >>> len(u'Andr\xe9')
    5

    >>> join('http://example.org/', u'#Andr\xe9')
    u'http://example.org/#Andr\xe9'
    """
    assert find(here, '#') < 0, "Base may not contain hash: '%s'" % here
    slashl = find(there, '/')
    colonl = find(there, ':')
    if colonl >= 0 and (slashl < 0 or colonl < slashl):
        return there
    bcolonl = find(here, ':')
    assert bcolonl >= 0, "Base uri '%s' is not absolute" % here
    if here[bcolonl + 1:bcolonl + 2] != '/':
        raise ValueError("Base <%s> has no slash after colon - with relative '%s'." % (here, there))
    if here[bcolonl + 1:bcolonl + 3] == '//':
        bpath = find(here, '/', bcolonl + 3)
    else:
        bpath = bcolonl + 1
    if bpath < 0:
        bpath = len(here)
        here = here + '/'
    if there[:2] == '//':
        return here[:bcolonl + 1] + there
    if there[:1] == '/':
        return here[:bpath] + there
    slashr = rfind(here, '/')
    (path, frag) = splitFragP(there)
    if not path:
        return here + frag
    while 1:
        if path[:2] == './':
            path = path[2:]
        if path == '.':
            path = ''
        elif path[:3] == '../' or path == '..':
            path = path[3:]
            i = rfind(here, '/', bpath, slashr)
            if i >= 0:
                here = here[:i + 1]
                slashr = i
        else:
            break

    return here[:slashr + 1] + path + frag


import re, string
commonHost = re.compile('^[-_a-zA-Z0-9.]+:(//[^/]*)?/[^/]*$')

def refTo(base, uri):
    """figure out a relative URI reference from base to uri

    >>> refTo('http://example/x/y/z', 'http://example/x/abc')
    '../abc'

    >>> refTo('file:/ex/x/y', 'file:/ex/x/q/r#s')
    'q/r#s'

    >>> refTo(None, 'http://ex/x/y')
    'http://ex/x/y'

    >>> refTo('http://ex/x/y', 'http://ex/x/y')
    ''

    Note the relationship between refTo and join:
    join(x, refTo(x, y)) == y
    which points out certain strings which cannot be URIs. e.g.
    >>> x='http://ex/x/y';y='http://ex/x/q:r';join(x, refTo(x, y)) == y
    0

    So 'http://ex/x/q:r' is not a URI. Use 'http://ex/x/q%3ar' instead:
    >>> x='http://ex/x/y';y='http://ex/x/q%3ar';join(x, refTo(x, y)) == y
    1

    This one checks that it uses a root-realtive one where that is
    all they share.  Now uses root-relative where no path is shared.
    This is a matter of taste but tends to give more resilience IMHO
    -- and shorter paths

    Note that base may be None, meaning no base.  In some situations, there
    just ain't a base. Slife. In these cases, relTo returns the absolute value.
    The axiom abs(,rel(b,x))=x still holds.
    This saves people having to set the base to "bogus:".

    >>> refTo('http://ex/x/y/z', 'http://ex/r')
    '/r'

    """
    if not base:
        return uri
    if base == uri:
        return ''
    i = 0
    while i < len(uri) and i < len(base):
        if uri[i] == base[i]:
            i = i + 1
        else:
            break

    m = commonHost.match(base[:i])
    if m:
        k = uri.find('//')
        if k < 0:
            k = -2
        l = uri.find('/', k + 2)
        if uri[l + 1:l + 2] != '/' and base[l + 1:l + 2] != '/' and uri[:l] == base[:l]:
            return uri[l:]
    if uri[i:i + 1] == '#' and len(base) == i:
        return uri[i:]
    while i > 0 and uri[(i - 1)] != '/':
        i = i - 1

    if i < 3:
        return uri
    if string.find(base, '//', i - 2) > 0 or string.find(uri, '//', i - 2) > 0:
        return uri
    if string.find(base, ':', i) > 0:
        return uri
    n = string.count(base, '/', i)
    if n == 0 and i < len(uri) and uri[i] == '#':
        return './' + uri[i:]
    elif n == 0 and i == len(uri):
        return './'
    else:
        return '../' * n + uri[i:]


import os

def base():
    """The base URI for this process - the Web equiv of cwd

        Relative or abolute unix-standard filenames parsed relative to
        this yeild the URI of the file.
        If we had a reliable way of getting a computer name,
        we should put it in the hostname just to prevent ambiguity

        """
    return 'file:' + _fixslash(os.getcwd()) + '/'


def _fixslash(str):
    """ Fix windowslike filename to unixlike - (#ifdef WINDOWS)"""
    s = str
    for i in range(len(s)):
        if s[i] == '\\':
            s = s[:i] + '/' + s[i + 1:]

    if s[0] != '/' and s[1] == ':':
        s = s[2:]
    return s


import unittest

class Tests(unittest.TestCase):

    def testPaths(self):
        cases = (
         ('foo:xyz', 'bar:abc', 'bar:abc'),
         ('http://example/x/y/z', 'http://example/x/abc', '../abc'),
         ('http://example2/x/y/z', 'http://example/x/abc', 'http://example/x/abc'),
         ('http://ex/x/y/z', 'http://ex/x/r', '../r'),
         ('http://ex/x/y', 'http://ex/x/q/r', 'q/r'),
         ('http://ex/x/y', 'http://ex/x/q/r#s', 'q/r#s'),
         ('http://ex/x/y', 'http://ex/x/q/r#s/t', 'q/r#s/t'),
         ('http://ex/x/y', 'ftp://ex/x/q/r', 'ftp://ex/x/q/r'),
         ('http://ex/x/y', 'http://ex/x/y', ''),
         ('http://ex/x/y/', 'http://ex/x/y/', ''),
         ('http://ex/x/y/pdq', 'http://ex/x/y/pdq', ''),
         ('http://ex/x/y/', 'http://ex/x/y/z/', 'z/'),
         ('file:/swap/test/animal.rdf', 'file:/swap/test/animal.rdf#Animal', '#Animal'),
         ('file:/e/x/y/z', 'file:/e/x/abc', '../abc'),
         ('file:/example2/x/y/z', 'file:/example/x/abc', '/example/x/abc'),
         ('file:/ex/x/y/z', 'file:/ex/x/r', '../r'),
         ('file:/ex/x/y/z', 'file:/r', '/r'),
         ('file:/ex/x/y', 'file:/ex/x/q/r', 'q/r'),
         ('file:/ex/x/y', 'file:/ex/x/q/r#s', 'q/r#s'),
         ('file:/ex/x/y', 'file:/ex/x/q/r#', 'q/r#'),
         ('file:/ex/x/y', 'file:/ex/x/q/r#s/t', 'q/r#s/t'),
         ('file:/ex/x/y', 'ftp://ex/x/q/r', 'ftp://ex/x/q/r'),
         ('file:/ex/x/y', 'file:/ex/x/y', ''),
         ('file:/ex/x/y/', 'file:/ex/x/y/', ''),
         ('file:/ex/x/y/pdq', 'file:/ex/x/y/pdq', ''),
         ('file:/ex/x/y/', 'file:/ex/x/y/z/', 'z/'),
         ('file:/devel/WWW/2000/10/swap/test/reluri-1.n3', 'file://meetings.example.com/cal#m1',
 'file://meetings.example.com/cal#m1'),
         ('file:/home/connolly/w3ccvs/WWW/2000/10/swap/test/reluri-1.n3', 'file://meetings.example.com/cal#m1',
 'file://meetings.example.com/cal#m1'),
         ('file:/some/dir/foo', 'file:/some/dir/#blort', './#blort'),
         ('file:/some/dir/foo', 'file:/some/dir/#', './#'),
         ('http://example/x/y%2Fz', 'http://example/x/abc', 'abc'),
         ('http://example/x/y/z', 'http://example/x%2Fabc', '/x%2Fabc'),
         ('http://example/x/y%2Fz', 'http://example/x%2Fabc', '/x%2Fabc'),
         ('http://example/x%2Fy/z', 'http://example/x%2Fy/abc', 'abc'),
         ('http://example/x/abc.efg', 'http://example/x/', './'))
        for (inp1, inp2, exp) in cases:
            self.assertEquals(refTo(inp1, inp2), exp)
            self.assertEquals(join(inp1, exp), inp2)

    def testSplit(self):
        cases = (
         ('abc#def', 'abc', 'def'),
         ('abc', 'abc', None),
         ('#def', '', 'def'),
         ('', '', None),
         ('abc#de:f', 'abc', 'de:f'),
         ('abc#de?f', 'abc', 'de?f'),
         ('abc#de/f', 'abc', 'de/f'))
        for (inp, exp1, exp2) in cases:
            self.assertEquals(splitFrag(inp), (exp1, exp2))

        return

    def testRFCCases(self):
        base = 'http://a/b/c/d;p?q'
        normalExamples = (
         (
          base, 'g:h', 'g:h'),
         (
          base, 'g', 'http://a/b/c/g'),
         (
          base, './g', 'http://a/b/c/g'),
         (
          base, 'g/', 'http://a/b/c/g/'),
         (
          base, '/g', 'http://a/g'),
         (
          base, '//g', 'http://g'),
         (
          base, '?y', 'http://a/b/c/?y'),
         (
          base, 'g?y', 'http://a/b/c/g?y'),
         (
          base, '#s', 'http://a/b/c/d;p?q#s'),
         (
          base, 'g#s', 'http://a/b/c/g#s'),
         (
          base, 'g?y#s', 'http://a/b/c/g?y#s'),
         (
          base, ';x', 'http://a/b/c/;x'),
         (
          base, 'g;x', 'http://a/b/c/g;x'),
         (
          base, 'g;x?y#s', 'http://a/b/c/g;x?y#s'),
         (
          base, '.', 'http://a/b/c/'),
         (
          base, './', 'http://a/b/c/'),
         (
          base, '..', 'http://a/b/'),
         (
          base, '../', 'http://a/b/'),
         (
          base, '../g', 'http://a/b/g'),
         (
          base, '../..', 'http://a/'),
         (
          base, '../../', 'http://a/'),
         (
          base, '../../g', 'http://a/g'))
        otherExamples = (
         (
          base, '', base),
         (
          base, '../../../g', 'http://a/g'),
         (
          base, '../../../../g', 'http://a/g'),
         (
          base, '/./g', 'http://a/./g'),
         (
          base, '/../g', 'http://a/../g'),
         (
          base, 'g.', 'http://a/b/c/g.'),
         (
          base, '.g', 'http://a/b/c/.g'),
         (
          base, 'g..', 'http://a/b/c/g..'),
         (
          base, '..g', 'http://a/b/c/..g'),
         (
          base, './../g', 'http://a/b/g'),
         (
          base, './g/.', 'http://a/b/c/g/.'),
         (
          base, 'g/./h', 'http://a/b/c/g/./h'),
         (
          base, 'g/../h', 'http://a/b/c/g/../h'),
         (
          base, 'g;x=1/./y', 'http://a/b/c/g;x=1/./y'),
         (
          base, 'g;x=1/../y', 'http://a/b/c/g;x=1/../y'),
         (
          base, 'g?y/./x', 'http://a/b/c/g?y/./x'),
         (
          base, 'g?y/../x', 'http://a/b/c/g?y/../x'),
         (
          base, 'g#s/./x', 'http://a/b/c/g#s/./x'),
         (
          base, 'g#s/../x', 'http://a/b/c/g#s/../x'))
        for (b, inp, exp) in normalExamples + otherExamples:
            if exp is None:
                self.assertRaises(ValueError, join, b, inp)
            else:
                self.assertEquals(join(b, inp), exp)

        return


def _test():
    import doctest, uripath
    doctest.testmod(uripath)
    unittest.main()


if __name__ == '__main__':
    _test()