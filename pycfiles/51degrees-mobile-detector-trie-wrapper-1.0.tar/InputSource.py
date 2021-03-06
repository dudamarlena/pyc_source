# uncompyle6 version 3.6.7
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: \Ft\Xml\InputSource.py
# Compiled at: 2005-09-14 19:06:15
__doc__ = '\nClasses providing a standard interface and encapsulation of metadata for\ndocument/entity streams intended for input to various XML processors.\n\nCopyright 2005 Fourthought, Inc. (USA).\nDetailed license and copyright information: http://4suite.org/COPYRIGHT\nProject home, documentation, distributions: http://4suite.org/\n'
import os, cStringIO, types, warnings, mimetools
from Ft import FtWarning
from Ft.Lib import Uri, Uuid
__all__ = [
 'InputSource', 'NullInputSource', 'InputSourceFactory', 'DefaultFactory', 'NoCatalogFactory']
_file_methods = (
 'read', 'readline', 'readlines', 'close')

class InputSource:
    """
    An input source is an encapsulation of a source of content.
    It includes a stream (Python file-like object) from which the
    content can be read, a URI to identify the stream and facilitate
    resolution of relative URI references / system IDs encountered
    within the stream, and parameters used by the processors of the
    stream (XML parsers, XSLT processors).

    It is designed to be overridden as applications need different
    functionality from sources.
    """
    __module__ = __name__
    RESOLVE_ENTITY_HINT = 'EXTERNAL ENTITY'
    RESOLVE_URI_HINT = 'RESOLVE URI'
    CATALOG_URI_HINT = 'CATALOG URI'

    def __init__(self, stream, uri=None, processIncludes=True, stripElements=None, factory=None, resolver=Uri.BASIC_RESOLVER, catalog=None, encoding=None):
        """
        InputSource constructor

        source = InputSource(...)

        stream - the stream associated with this input source
        uri - the absolute URI of the input source
        processIncludes - Whether or not XIncludes should be expanded
        stripElements - Space stripping rules
        factory - The factory that created this instance
        resolver - URI resolver; defaults to Ft.Lib.Uri.BASIC_RESOLVER
        catalog - TR9401/XML Catalog object for resolving public IDs
        encoding - a string externally declaring the stream's encoding
        """
        if uri:
            self.uri = uri
        else:
            self.uri = 'urn:uuid:' + Uuid.UuidAsString(Uuid.GenerateUuid())
        self.stream = stream
        self.processIncludes = processIncludes
        self.stripElements = stripElements or []
        self.factory = factory
        self.fragment = Uri.SplitFragment(self.uri)[1]
        self._resolver = resolver
        self._catalog = catalog
        enc = self._getStreamEncoding(stream)
        if enc is None:
            enc = encoding
        self.encoding = enc
        self.name = self.uri
        for name in _file_methods:
            method = getattr(stream, name, None)
            if method:
                setattr(self, name, method)

        return
        return

    def _getStreamEncoding(self, stream):
        """
        Returns the encoding of the given stream, if this info can be
        determined from metadata in the stream object with a reasonable
        degree of confidence.

        Adheres to RFC 3023, which requires the the charset value in the
        Content-Type header to take precedence, or if no value is
        available, to assume us-ascii in the case of certain text/*
        media types. For other text/* media types, adheres to RFC 2616
        sec. 3.7.1, which requires the assumption of iso-8859-1, when
        the entity was transmitted by HTTP. Media type and charset info
        is ignored for streams believed to originate from a local file,
        in accordance with XML 1.0 Third Edition appendix F.2.
        """
        stream_url = getattr(stream, 'url', None)
        if stream_url is None:
            return None
        scheme = Uri.GetScheme(stream_url)
        if scheme is None or scheme.lower() in ('file', 'ftp') or len(scheme) == 1:
            return None
        info = None
        if hasattr(self.stream, 'info'):
            if isinstance(self.stream.info, types.MethodType):
                info = self.stream.info()
        if isinstance(info, mimetools.Message):
            charset = info.getparam('charset')
            if charset:
                return charset
            maintype = getattr(info, 'maintype', None)
            subtype = getattr(info, 'subtype', None)
            if maintype == 'text':
                if subtype == 'xml' or subtype == 'xml-external-parsed-entity' or subtype.endswith('+xml'):
                    return 'us-ascii'
                elif scheme == 'http':
                    return 'iso-8859-1'
        return None
        return

    def resolveEntity(self, publicId, systemId):
        """
        Resolve an external entity to a new InputSource.

        Presented with an optional public identifier and a system identifier,
        this function attempts to locate a mapping in the catalog, if one is
        defined.  If no mapping is found, the system identifier will be
        dereferenced as a URL.
        """
        hint = InputSource.RESOLVE_ENTITY_HINT
        if self._catalog:
            new_uri = self._catalog.resolveEntity(publicId, systemId)
            if new_uri is not None:
                systemId = new_uri
                hint = InputSource.CATALOG_URI_HINT
        return self._resolve(systemId, None, hint)
        return

    def resolve(self, uri, base=None, hint=None):
        """
        Resolve a URI reference into a new InputSource.
        
        This function is used when a URI reference is encountered in the
        original stream and needs to be resolved (e.g. xi:include,
        xsl:include, xsl:import, document(), etc.).  When a catalog is
        available, its URI entries are used first.  If no entry is found,
        the URI is resolved against the current URI and then opened.
        
        The hint parameter is used to give a hint as to what the
        resolution will be used for.

        If the ignoreErrors flag is set, an error during resolution
        (such as "file not found") will result in None's being returned,
        rather than a raised exception.
        """
        if self._catalog:
            new_uri = self._catalog.resolveURI(uri)
            if new_uri is not None:
                uri = new_uri
                hint = InputSource.CATALOG_URI_HINT
        if hint is None:
            hint = InputSource.RESOLVE_URI_HINT
        return self._resolve(uri, base, hint)
        return

    def getUriResolver(self):
        """
        This method returns the URI resolver that is used by this
        input source to normalize (resolve to absolute form) and
        resolve (dereference) URI references. This is the public method
        to use if just URI resolution is needed.
        """
        return self._resolver

    def _resolve(self, uri, base, hint, ignoreErrors=False):
        """
        Resolves a system identifier (fragmentless URI reference) into a
        new input source.

        The hint parameter is used to give a hint as to what the
        resolution will be used for.

        If the ignoreErrors flag is set, an error during resolution
        (such as "file not found") will result in None's being returned,
        rather than a raised exception.
        """
        uri = self._normalize(uri, base)
        stream = self._openStream(uri, ignoreErrors, hint)
        return self.clone(stream, uri, hint)

    def _normalize(self, uriref, base=None):
        """
        Normalize (resolve to absolute form) a given URI reference,
        using the URI of this input source as the base.

        The default implementation will just use the default URI resolver.

        If your input source is working with non-standard or not supported
        URIs, then you will need to override this or the getUriResolver method.
        """
        if base is None:
            base = self.uri
        return self.getUriResolver().normalize(uriref, base)
        return

    def _openStream(self, uri, ignoreErrors=False, hint=None):
        """
        Returns a representation of a resource as a stream by
        resolving the given URI. If ignoreErrors is set, failure to
        obtain the stream will result in None being returned, rather
        than an exception (e.g. "file not found") being raised.

        Default behaviour is to use the resolver associated with this
        InputSource. If your custom InputSource needs to open URIs
        that are not supported natively by this InputSource (e.g.,
        repository objects, or objects from a database), then you
        should override this method and do whatever it takes to
        resolve the URI into a readable stream.
        """
        try:
            return self.getUriResolver().resolve(uri)
        except:
            if ignoreErrors:
                return None
            raise

        return

    def clone(self, stream, uri=None, hint=None):
        """
        Clones this input source, creating a new instance with
        the known params.

        If your derived InputSource requires additional state information
        then you have to override how it is cloned and pickled.
        """
        if uri is None:
            uri = self.uri
        if stream is None:
            return NullInputSource(uri)
        if hint is not None:
            encoding = None
        else:
            encoding = self.encoding
        return self.__class__(stream, uri, processIncludes=self.processIncludes, stripElements=self.stripElements, factory=self.factory, resolver=self._resolver, catalog=self._catalog, encoding=encoding)
        return

    def __getstate__(self):
        state = self.__dict__.copy()
        state['stream'] = None
        return state
        return


class NullInputSource(InputSource):
    """
    An InputSource that simulates an empty stream.
    """
    __module__ = __name__

    def __init__(self, uri=None):
        InputSource.__init__(self, cStringIO.StringIO(), uri)


class InputSourceFactory:
    """
    A factory for creating new InputSource instances.
    """
    __module__ = __name__
    FACTORY_URI_HINT = 'FACTORY URI'

    def __init__(self, inputSourceClass=None, resolver=Uri.BASIC_RESOLVER, catalog=None):
        self._klass = inputSourceClass or InputSource
        self.resolver = resolver
        self.catalog = catalog
        return

    def fromUri(self, uri, *v_args, **kw_args):
        r"""
        Creates an InputSource from the stream resulting from the
        resolution of the given URI.

        uri - a URI from which the input will be read.  Important: a file
              path is generally not a URI. To be safe, if you wish to read
              from a file, use the following pattern:
              from Ft.Lib import Uri
              uri = Uri.OsPathToUri("/path/to/file.ext")
              OR uri = Uri.OsPathToUri("C:\path\to\file.ext")
        """
        hint = InputSourceFactory.FACTORY_URI_HINT
        if self.catalog:
            new_uri = self.catalog.resolveURI(uri)
            if new_uri is not None:
                uri = new_uri
                hint = InputSource.CATALOG_URI_HINT
        src = self.fromStream(None, uri, *v_args, **kw_args)
        return src._resolve(uri, None, hint)
        return

    def fromString(self, st, uri=None, *v_args, **kw_args):
        """
        Creates an InputSource from a stream derived from the given
        string. The uri argument is the URI to use for the stream
        (one should always be given, even if it's bogus).
        """
        if not isinstance(st, str):
            raise ValueError('String must be of type string, not %s' % (st is None and 'None' or type(st).__name__))
        stream = cStringIO.StringIO(st)
        return self.fromStream(stream, uri, *v_args, **kw_args)
        return

    def fromStream(self, stream, uri=None, *v_args, **kw_args):
        """
        Creates an InputSource from the given stream.
        The uri argument is the URI to use for the stream
        (one should always be given, even if it's bogus).
        """
        if not uri:
            warnings.warn('Creation of InputSource without a URI', FtWarning, 2)
        kw_args['factory'] = self
        if 'resolver' not in kw_args:
            kw_args['resolver'] = self.resolver
        if 'catalog' not in kw_args:
            kw_args['catalog'] = self.catalog
        return self._klass(stream, uri, *v_args, **kw_args)


NoCatalogFactory = InputSourceFactory(catalog=None)
from Ft.Xml.Catalog import GetDefaultCatalog
DefaultFactory = InputSourceFactory(catalog=GetDefaultCatalog())