# uncompyle6 version 3.7.4
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: \Ft\Xml\Catalog.py
# Compiled at: 2006-08-12 10:56:22
"""
Classes and functions that help implement OASIS XML and TR9401 Catalogs.
Resolution with Catalogs is handled via the Ft.Xml.InputSource module.

Based on a contribution to PyXML from Tarn Weisner Burton
<twburton@users.sf.net>. See
http://sourceforge.net/tracker/index.php?func=detail&aid=490069&group_id=6473&atid=306473

Copyright 2005 Fourthought, Inc. (USA).
Detailed license and copyright information: http://4suite.org/COPYRIGHT
Project home, documentation, distributions: http://4suite.org/
"""
import os, re, sys, warnings, cStringIO
from xml.sax import xmlreader
from Ft import FtWarning, GetConfigVar
from Ft.Lib import Uri, UriException, ImportUtil
from Ft.Xml import XML_NAMESPACE
from Ft.Xml.Lib.XmlString import IsXml
__all__ = [
 'Catalog', 'GetDefaultCatalog']
TR9401 = re.compile('^\\s*(BASE|CATALOG|DELEGATE|PUBLIC|SYSTEM|OVERRIDE\\s+YES|OVERRIDE\\s+NO)\\s+"((?:[^"\\\\]|\\\\.)*)"(?:\\s+"((?:[^"\\\\]|\\\\.)*)")?', re.M | re.I)
_urn_hex_re = re.compile('%(..)')
_urn_trans_re = re.compile('[+:;]')
_urn_trans_map = {'+': ' ', ';': '//', ':': '::'}

def UnwrapUrn(urn):
    unwrapped = False
    if urn:
        if urn.lower()[:4] == 'urn:':
            parts = urn.split(':', 2)
            parts[:2] = [ x.lower() for x in parts[:2] ]
            urn = (':').join(parts)
            urn = _urn_hex_re.sub(lambda m: '%' + m.group(1).upper(), urn)
        if urn[:13] == 'urn:publicid:':
            urn = urn[13:]
            urn = _urn_trans_re.sub(lambda m: _urn_trans_map[m.group()], urn)
            urn = _urn_hex_re.sub(lambda m: chr(int(m.group(1), 16)), urn)
            unwrapped = True
    return (
     unwrapped, urn)


class Catalog:
    """
    Reads and provides access to a catalog, providing mappings of public
    and system IDs to URIs, etc.

    It is implemented as a SAX ContentHandler and is able to read
    OASIS TR 9401 Catalogs <http://www.oasis-open.org/specs/a401.htm>
    and OASIS XML Catalogs <http://www.oasis-open.org/committees/entity/spec.html>
    """
    __module__ = __name__

    def __init__(self, uri, quiet=True):
        self.systemIds = {}
        self.publicIds = {}
        self.uris = {}
        self.publicDelegates = []
        self.systemDelegates = []
        self.uriDelegates = []
        self.systemRewrites = []
        self.uriRewrites = []
        self.catalogs = []
        self.uri = uri
        self.quiet = quiet
        if not Uri.IsAbsolute(uri):
            warnings.warn("Catalog URI '%s' is not absolute.", FtWarning, 2)
        stream = Uri.BASIC_RESOLVER.resolve(uri)
        data = stream.read()
        stream.close()
        if IsXml(data):
            self._parseXmlCat(data)
        else:
            self._parseTr9401(data)
        self.publicDelegates.sort()
        self.publicDelegates.reverse()
        self.systemDelegates.sort()
        self.systemDelegates.reverse()
        self.uriDelegates.sort()
        self.uriDelegates.reverse()
        self.systemRewrites.sort()
        self.systemRewrites.reverse()
        self.uriRewrites.sort()
        self.uriRewrites.reverse()
        if not quiet:
            sys.stderr.write('Catalog contents:\n')
            for key in self.__dict__.keys():
                sys.stderr.write('  %s = %r\n' % (key, self.__dict__[key]))

            sys.stderr.flush()
        return

    def resolveEntity(self, publicId, systemId):
        """
        Return the applicable URI.

        If an external identifier (PUBLIC or SYSTEM) entry exists in the
        Catalog for the identifier(s) specified, return the mapped value.

        External identifiers identify the external subset, entities, and
        notations of an XML document.
        """
        (unwrapped, publicId) = UnwrapUrn(publicId)
        (unwrapped, systemId) = UnwrapUrn(systemId)
        if unwrapped:
            if not publicId:
                publicId = systemId
                systemId = None
            elif publicId == systemId:
                systemId = None
            else:
                warnings.warn('publicId %r does not match the unwrapped systemId %r' % (publicId, systemId), FtWarning, 2)
                systemId = None
        if systemId is not None:
            if systemId in self.systemIds:
                return self.systemIds[systemId]
            for (length, start, rewrite) in self.systemRewrites:
                if start == systemId[:length]:
                    return rewrite + systemId[length:]

            attempted = False
            for (length, start, catalog) in self.systemDelegates:
                if start == systemId[:length]:
                    attempted = True
                    result = catalog.resolveEntity(publicId, systemId)
                    if result:
                        return result

            if attempted:
                return
        if publicId is not None:
            if publicId in self.publicIds:
                (uri, prefer) = self.publicIds[publicId]
                if systemId is None or prefer:
                    return uri
            attempted = False
            for (length, start, catalog, prefer) in self.publicDelegates:
                if (systemId is None or prefer) and start == publicId[:length]:
                    attempted = True
                    result = catalog.resolveEntity(publicId, systemId)
                    if result:
                        return result

            if attempted:
                return
        for catalog in self.catalogs:
            result = catalog.resolveEntity(publicId, systemId)
            if result:
                return result

        return
        return

    def resolveURI(self, uri):
        """
        Return the applicable URI.

        If a URI entry exists in the Catalog for the URI specified, return
        the mapped value.

        URI references, for example namespace names, stylesheets, included
        files, graphics, and hypertext references, simply identify other
        resources.
        """
        (unwrapped, publicId) = UnwrapUrn(uri)
        if unwrapped:
            return self.resolveEntity(publicId, None)
        if uri in self.uris:
            return self.uris[uri]
        for (length, start, rewrite) in self.uriRewrites:
            if start == uri[:length]:
                return rewrite + uri[length:]

        attempted = False
        for (length, start, catalog) in self.uriDelegates:
            if start == uri[:length]:
                attempted = True
                result = catalog.resolveURI(uri)
                if result:
                    return result

        if attempted:
            return
        for catalog in self.catalogs:
            result = catalog.resolveURI(uri)
            if result:
                return result

        return
        return

    def _parseXmlCat(self, data):
        """
        Parse an XML Catalog, as specified in
        http://www.oasis-open.org/committees/entity/spec-2001-08-06.html.
        Partially implemented.
        """
        self.prefer_public = [
         True]
        self.base = [self.uri]
        source = xmlreader.InputSource(self.uri)
        source.setByteStream(cStringIO.StringIO(data))
        from Ft.Xml.Sax import CreateParser
        p = CreateParser()
        p.setFeature('http://xml.org/sax/features/external-parameter-entities', False)
        p.setContentHandler(self)
        p.parse(source)
        del self.prefer_public
        del self.base
        return

    def _parseTr9401(self, data):
        """
        Parse a TR9401 Catalog, as specified in
        <http://www.oasis-open.org/specs/a401.htm>.
        Partially implemented.
        """
        prefer_public = True
        base = self.uri
        for cmd in TR9401.findall(data):
            token = cmd[0].upper()
            if token == 'PUBLIC':
                if len(cmd) == 3:
                    self.publicIds[cmd[1]] = (
                     Uri.Absolutize(cmd[2], base), prefer_public)
            elif token == 'SYSTEM':
                if len(cmd) == 3:
                    self.systemIds[cmd[1]] = Uri.Absolutize(cmd[2], base)
            elif token == 'BASE':
                base = cmd[1]
            elif token[:8] == 'OVERRIDE':
                prefer_public = token[8:].strip() == 'YES'
            elif token == 'DELEGATE':
                if len(cmd) == 3:
                    self.publicDelegates[cmd[1]] = Uri.Absolutize(cmd[2], base)
            elif token == 'CATALOG':
                if len(cmd) == 2:
                    catalog = Catalog(Uri.Absolutize(cmd[1], base), self.quiet)
                    self.catalogs.append(catalog)

        return

    def startElementNS(self, (namespace, name), qualifiedName, attrs):
        """
        Handle an element start event for the XML parser.
        This is a SAX ContentHandler method.
        """
        base = self.base[(-1)]
        if name not in ('rewriteSystem', 'rewriteURI'):
            base = attrs.get((XML_NAMESPACE, 'base'), base)
        self.base.append(base)
        if name == 'public':
            if self.__ensure_attrs(name, attrs, 'publicId', 'uri'):
                publicId = attrs[(None, 'publicId')]
                uri = Uri.Absolutize(attrs[(None, 'uri')], base)
                self.publicIds[publicId] = (uri, self.prefer_public[(-1)])
        elif name == 'system':
            if self.__ensure_attrs(name, attrs, 'systemId', 'uri'):
                systemId = attrs[(None, 'systemId')]
                uri = Uri.Absolutize(attrs[(None, 'uri')], base)
                self.systemIds[systemId] = uri
        elif name == 'uri':
            if self.__ensure_attrs(name, attrs, 'name', 'uri'):
                name = attrs[(None, 'name')]
                uri = Uri.Absolutize(attrs[(None, 'uri')], base)
                self.uris[name] = uri
        elif name == 'rewriteURI':
            if self.__ensure_attrs(name, attrs, 'uriStartString', 'rewritePrefix'):
                startString = attrs[(None, 'uriStartString')]
                rewritePrefix = Uri.Absolutize(attrs[(None, 'rewritePrefix')], base)
                rewriteRule = (len(startString), startString, rewritePrefix)
                self.uriRewrites.append(rewriteRule)
        elif name == 'rewriteSystem':
            if self.__ensure_attrs(name, attrs, 'systemIdStartString', 'rewritePrefix'):
                startString = attrs[(None, 'systemIdStartString')]
                rewritePrefix = Uri.Absolutize(attrs[(None, 'rewritePrefix')], base)
                rewriteRule = (len(startString), startString, rewritePrefix)
                self.systemRewrites.append(rewriteRule)
        elif name == 'delegateSystem':
            if self.__ensure_attrs(name, attrs, 'systemIdStartString', 'catalog '):
                startString = attrs[(None, 'systemIdStartString')]
                catalog = Uri.Absolutize(attrs[(None, 'catalog')], base)
                delegate = Catalog(catalog, self.quiet)
                delegateRule = (len(startString), startString, delegate)
                self.systemDelegates.append(delegateRule)
        elif name == 'delegatePublic':
            if self.__ensure_attrs(name, attrs, 'publicIdStartString', 'catalog '):
                startString = attrs[(None, 'publicIdStartString')]
                catalog = Uri.Absolutize(attrs[(None, 'catalog')], base)
                delegate = Catalog(catalog, self.quiet)
                delegateRule = (len(startString), startString, delegate, self.prefer_public[(-1)])
                self.publicDelegates.append(delegateRule)
        elif name == 'delegateURI':
            if self.__ensure_attrs(name, attrs, 'uriStartString', 'catalog '):
                startString = attrs[(None, 'uriStartString')]
                catalog = Uri.Absolutize(attrs[(None, 'catalog')], base)
                delegate = Catalog(catalog, self.quiet)
                delegateRule = (len(startString), startString, delegate)
                self.uriDelegates.append(delegateRule)
        elif name == 'nextCatalog':
            if self.__ensure_attrs(name, attrs, 'catalog'):
                catalog = Uri.Absolutize(attrs[(None, 'catalog')], base)
                self.catalogs.append(Catalog(catalog, self.quiet))
        elif name in ('catalog', 'group'):
            prefer = self.prefer_public[(-1)] and 'public' or 'system'
            prefer = attrs.get((None, 'prefer'), prefer) == 'public'
            self.prefer_public.append(prefer)
        return
        return

    def __ensure_attrs(self, name, attrs, *attr_names):
        """
        Ensure that the right attributes exist just in case the parser
        is a non-validating one.
        """
        for attr_name in attr_names:
            if not attrs.has_key((None, attr_name)):
                if not self.quiet:
                    print '%s: Malformed %s element, missing %s attribute' % (self.uri, name, attr_name)
                return False

        return True
        return

    def endElementNS(self, (namespace, name), qualifiedName):
        """
        Handle an element end event for the XML parser.
        This is a SAX ContentHandler method.
        """
        self.base.pop()
        if name in ('catalog', 'group'):
            self.prefer_public.pop()
        return


def GetDefaultCatalog(basename='default.cat'):
    """
    Load the default catalog file(s).
    """
    quiet = 'XML_DEBUG_CATALOG' not in os.environ
    uris = []
    if 'XML_CATALOGS' in os.environ:
        for path in os.environ['XML_CATALOGS'].split(os.pathsep):
            uris.append(Uri.OsPathToUri(path))

    if 'XML_CATALOG_FILES' in os.environ:
        for path in os.environ['XML_CATALOG_FILES'].split():
            if not Uri.IsAbsolute(path):
                uris.append(Uri.OsPathToUri(path))
            else:
                uris.append(path)

    pathname = os.path.join(GetConfigVar('DATADIR'), basename)
    if GetConfigVar('RESOURCEBUNDLE'):
        resource = ImportUtil.OsPathToResource(pathname)
        uri = Uri.ResourceToUri('Ft.Xml', resource)
    else:
        uri = Uri.OsPathToUri(pathname)
    uris.append(uri)
    if not quiet:
        prefix = 'Catalog URIs:'
        for uri in uris:
            sys.stderr.write('%s %s\n' % (prefix, uri))
            prefix = ' ' * len(prefix)

    catalog = None
    for uri in uris:
        if not quiet:
            sys.stderr.write('Reading %s\n' % uri)
            sys.stderr.flush()
        try:
            if catalog is None:
                if not quiet:
                    sys.stderr.write('Creating catalog from %s\n' % uri)
                    sys.stderr.flush()
                catalog = Catalog(uri, quiet)
            else:
                if not quiet:
                    sys.stderr.write('Appending %s\n' % uri)
                    sys.stderr.flush()
                catalog.catalogs.append(Catalog(uri, quiet))
        except UriException, e:
            warnings.warn('Catalog resource (%s) disabled: %s' % (uri, e.message), FtWarning)

    if not quiet:
        sys.stderr.write('Done. Result is %r\n' % catalog)
        sys.stderr.flush()
    return catalog
    return