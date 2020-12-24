# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/Products/pluggablecatalog/interfaces.py
# Compiled at: 2008-07-23 15:36:19
from zope import interface

class IQueryDefaults(interface.Interface):
    """A component that adds default query parameters."""
    __module__ = __name__

    def __call__(context, request, args):
        """Returns a dictionary of query arguments which are used by
       the catalog in 'searchResults'.

         - `context` is the context in which the request was made.

         - `request` is the REQUEST as passed to
           `CatalogTool.searchResults`.

         - `args` is a dictionary that holds all search request info.
           It contains arguments from request and kwargs passed to
           `CatalogTool.searchResults`.
       """
        pass


class IQueryOverrides(interface.Interface):
    """A component that overrides query parameters."""
    __module__ = __name__

    def __call__(context, request, args):
        """See IQueryDefaults.__call__"""
        pass