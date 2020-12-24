# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/inquant/contentmirror/base/traverser.py
# Compiled at: 2008-04-25 10:45:09
__author__ = 'Stefan Eletzhofer <stefan.eletzhofer@inquant.de>'
__docformat__ = 'plaintext'
__revision__ = '$Revision: 63520 $'
__version__ = '$Revision: 63520 $'[11:-2]
from zope import component
from zope import interface
from zope.publisher.interfaces import NotFound
from zope.publisher.interfaces import IPublishTraverse
from zope.publisher.http import IHTTPRequest
from ZPublisher.BaseRequest import DefaultPublishTraverse
from Acquisition import aq_inner, aq_base
from Products.CMFCore.utils import getToolByName
from inquant.contentmirror.base.interfaces import IMirrorContentLocator
from inquant.contentmirror.base.utils import give_new_context
from inquant.contentmirror.base.utils import info, debug

class MirrorObjectTraverser(object):
    """
    A traverser which tries to locate mirrored objects. If such a object can be
    located (by querying the IMirrorObjectLocator), then the object returned by
    the locator is inserted into the context's acquisition chain.
    """
    __module__ = __name__
    interface.implements(IPublishTraverse)

    def __init__(self, context, request):
        self.locator = IMirrorContentLocator(context)
        self.default = DefaultPublishTraverse(context, request)
        self.context = context
        self.request = request

    def publishTraverse(self, request, name):
        try:
            obj = self.default.publishTraverse(request, name)
            return obj
        except (NotFound, AttributeError), e:
            context = aq_inner(self.context)
            info('MirrorObjectTraverser: default traverser returned NotFound. %s -> %s' % (self.context, name))
            obj = self.locator.locate(name)
            if obj is None:
                raise e
            obj = give_new_context(obj, context)
            info('MirrorObjectTraverser: ctx %s, name %s -> %s' % (context, name, obj))
            return obj

        return