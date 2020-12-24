# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/max/development/checkouts/inqbus.collection.proxy/inqbus/collection/proxy/traversal.py
# Compiled at: 2011-06-07 07:02:24
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from zope.component import adapts, getMultiAdapter
from zope.component import queryMultiAdapter
from zope.site.hooks import getSite
from zope.app.publisher.browser import getDefaultViewName
from zope.interface import alsoProvides, Interface
from zope.publisher.interfaces.http import IHTTPRequest
from zope.publisher.interfaces import NotFound
from ZPublisher.BaseRequest import DefaultPublishTraverse
from Products.CMFCore.utils import getToolByName
from Acquisition import aq_base, aq_inner
from inqbus.collection.proxy.browser.collectionproxyview import CollectionProxyView
import logging
log = logging.getLogger('inqbus.collection.proxy')

class CollectionProxyTraverser(DefaultPublishTraverse):
    """
    """
    adapts(IHTTPRequest)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def publishTraverse(self, request, name):
        if hasattr(self.context, 'boolean_proxy_field') and self.context.boolean_proxy_field:
            try:
                return super(CollectionProxyTraverser, self).publishTraverse(request, name)
            except (NotFound, AttributeError), e:
                self.request = request
                self.request.set('disable_border', True)
                keywords = []
                keyword_count = 0
                while self.hasMoreNames():
                    keywords.append(name)
                    keyword_count += 1
                    name = self.nextName()

                if not name.startswith('@@'):
                    keywords.append(name)
                if not len(keywords):
                    return
                keywords.pop(0)
                proxy_relpath = ('/').join(keywords)
                source_object = self.get_source_object(proxy_relpath)
                if source_object:
                    source_object = aq_base(source_object)
                    source_object = source_object.__of__(self.context)
                    return source_object
                raise e

        else:
            return super(CollectionProxyTraverser, self).publishTraverse(request, name)

    def nextName(self):
        """Pop the next name off of the traversal stack.
        """
        return self.request['TraversalRequestNameStack'].pop()

    def hasMoreNames(self):
        """Are there names left for traversal?
        """
        viewlists = [
         'view', 'edit']
        return len(self.request['TraversalRequestNameStack']) > 0 and self.request['TraversalRequestNameStack'][(-1)] not in viewlists

    def get_source_object(self, relpath=''):
        """ return object from source_folder.
        """
        source_object = getSite().unrestrictedTraverse(relpath, None)
        if source_object:
            return source_object
        else:
            log.info('source_object not found!')
            return
            return