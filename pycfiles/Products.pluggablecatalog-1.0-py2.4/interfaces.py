# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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