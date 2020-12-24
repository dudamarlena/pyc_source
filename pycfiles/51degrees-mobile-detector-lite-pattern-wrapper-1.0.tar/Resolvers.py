# uncompyle6 version 3.6.7
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: \Ft\Lib\Resolvers.py
# Compiled at: 2005-01-05 05:04:22
__doc__ = '\nSpecialized and useful URI resolvers\n\nCopyright 2005 Fourthought, Inc. (USA).\nDetailed license and copyright information: http://4suite.org/COPYRIGHT\nProject home, documentation, distributions: http://4suite.org/\n'
import os, sys, cStringIO
from Ft.Lib import Uri

class SchemeRegistryResolver(Uri.FtUriResolver):
    """
    A type of resolver that allows developers to register different callable
    objects to handle different URI schemes.  The default action if there
    is nothing registered for the scheme will be to fall back to
    UriResolverBase behavior *unless* you have in the mapping a special
    scheme None.  The callable object that is the value on that key will
    then be used as the default for all unknown schemes.

    The expected function signature for scheme call-backs matches
    UriResolverBase.resolve, without the instance argument:

    resolve(uri, base=None)

    Reminder: Since this does not include self, if you are registering
    a method, use the method instance (i.e. myresolver().handler
    rather than myresolver.handler)

    You can manipulate the mapping directly using the "handlers" attribute.
    """
    __module__ = __name__

    def __init__(self, handlers=None):
        """
        handlers - a Python dictionary with scheme names as keys (e.g. "http")
        and callable objects as values
        """
        Uri.UriResolverBase.__init__(self)
        self.handlers = handlers or {}
        return

    def resolve(self, uri, base=None):
        scheme = Uri.GetScheme(uri)
        if not scheme:
            if base:
                scheme = Uri.GetScheme(base)
            if not scheme:
                raise Uri.UriException(Uri.UriException.SCHEME_REQUIRED, base=base, ref=uri)
        func = self.handlers.get(scheme)
        if not func:
            func = self.handlers.get(None)
            if not func:
                return Uri.UriResolverBase.resolve(self, uri, base)
        return func(uri, base)
        return


Uri.SchemeRegistryResolver = SchemeRegistryResolver

class FacadeResolver(Uri.FtUriResolver):
    """
    A type of resolver that can be used to create a facade or cache of
    resources by keeping a dictionary of URI to result mappings.  When a
    URI is provided for resolution, the mapping is first checked, and a
    stream is constructed by wrapping the mapping value string.
    If no match is found in the mapping, fall back to the standard
    resolver logic.

    You can manipulate the mapping directly using the "cache" attribute.
    """
    __module__ = __name__

    def __init__(self, cache=None, observer=None):
        """
        cache - a dictionary with mapings from URI to value (as an object
        to be converted to a UTF-8 encoded string)
        observer - callable object invoked on each resolution request
        """
        Uri.UriResolverBase.__init__(self)
        self.cache = cache or {}
        self.observer = observer
        return

    def resolve(self, uri, base=None):
        self.observer(uri, base)
        if uri in self.cache:
            cachedval = self.cache[uri]
            if isinstance(cachedval, unicode):
                return cStringIO.StringIO(cachedval.encode('utf-8'))
            else:
                return cStringIO.StringIO(str(cachedval))
        return Uri.UriResolverBase.resolve(self, uri, base)