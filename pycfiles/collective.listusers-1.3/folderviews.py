# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/collective/listjs/browser/folderviews.py
# Compiled at: 2011-11-01 10:41:40
from zope.interface import Interface, implements
from zope import schema
from Products.Five import BrowserView
from Products.ATContentTypes.interface import IATTopic

class IListJsEnabledFolderView(Interface):
    """A List.js enabled folder view
    """
    contents = schema.Object(Interface)


class ListJsEnabledFolderView(BrowserView):
    """An Plone implementation of a List.js folder View,
    with AJAX niceness.
    """
    implements(IListJsEnabledFolderView)

    def query(self, start, limit, contentFilter):
        """ Make catalog query for the folder listing.
    
        @param start: First index to query
    
        @param limit: maximum number of items in the batch
    
        @param contentFilter: portal_catalog filtering dictionary with index -> value pairs.
    
        @return: Products.CMFPlone.PloneBatch.Batch object
        """
        b_size = limit
        b_start = start
        if IATTopic.providedBy(self.context):
            return self.context.queryCatalog(contentFilter, batch=True, b_size=b_size)
        else:
            return self.context.getFolderContents(contentFilter, batch=True, b_size=b_size)

    def __call__(self):
        """ Render the content item listing.
        """
        limit = 100
        filter = {}
        start = self.request.get('b_start', 0)
        self.contents = self.query(start, limit, filter)
        return self.index()