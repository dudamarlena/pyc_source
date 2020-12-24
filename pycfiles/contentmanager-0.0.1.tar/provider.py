# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/contentlet/provider.py
# Compiled at: 2010-05-23 04:49:48
__doc__ = ' Implementations of IContentProvider.'
from zope.interface import providedBy
from zope.component import getGlobalSiteManager
from contentlet.interfaces import IContentProvider
__all__ = [
 'query_provider',
 'get_provider']

def query_provider(name, context=None, registry=None):
    """ Query content provider by `name`."""
    if registry is None:
        registry = getGlobalSiteManager()
    provider = registry.adapters.lookup((
     providedBy(context),), IContentProvider, name=name, default=None)
    return provider


def get_provider(name, context=None, registry=None):
    """ Get content provider by `name` or raise LookupError."""
    provider = query_provider(name, context=context, registry=registry)
    if provider is None:
        raise LookupError("No provider was found for name '%s'" % name)
    return provider