# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /zerodb/collective/indexing/indexer.py
# Compiled at: 2016-03-04 03:26:39
from zope.interface import implementer
from zerodb.collective.indexing.interfaces import IIndexQueueProcessor

class IPortalCatalogQueueProcessor(IIndexQueueProcessor):
    """ an index queue processor for the standard portal catalog via
        the `CatalogMultiplex` and `CMFCatalogAware` mixin classes """
    pass


@implementer(IPortalCatalogQueueProcessor)
class PortalCatalogProcessor(object):

    def index(self, obj, attributes=None):
        pass

    def reindex(self, obj, attributes=None):
        pass

    def unindex(self, obj):
        pass

    def begin(self):
        pass

    def commit(self):
        pass

    def abort(self):
        pass