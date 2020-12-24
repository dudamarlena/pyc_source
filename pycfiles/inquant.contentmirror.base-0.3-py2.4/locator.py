# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/inquant/contentmirror/base/locator.py
# Compiled at: 2008-04-25 11:52:35
__author__ = 'Stefan Eletzhofer <stefan.eletzhofer@inquant.de>'
__docformat__ = 'plaintext'
__revision__ = '$Revision: 63530 $'
__version__ = '$Revision: 63530 $'[11:-2]
import logging
from zope import component
from zope import interface
from zope.annotation.interfaces import IAnnotations, IAttributeAnnotatable
from persistent.dict import PersistentDict
from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName
from inquant.contentmirror.base.interfaces import IMirrorContentProvider
from inquant.contentmirror.base.interfaces import IMirrorContentLocator
from inquant.contentmirror.base.interfaces import IMirrorUIDManager
from inquant.contentmirror.base.utils import info, debug, error

class UIDLocator(object):
    __module__ = __name__
    interface.implements(IMirrorContentLocator)

    def __init__(self, context):
        self.context = context
        self.uic = getToolByName(context, 'uid_catalog')

    def locate(self, name):
        context = aq_inner(self.context)
        debug('UIDTraverser: trying to locate %s (context %s)' % (name, self.context))
        manager = component.queryAdapter(context, IMirrorUIDManager)
        if not manager:
            error('UIDTraverser: no UID manager')
            return
        uid = manager.get(name, None)
        if not uid:
            error("UIDTraverser: no UID found for '%s'" % name)
            return
        debug('UIDTraverser: UID: %s' % uid)
        res = self.uic(UID=uid)
        if not len(res):
            debug('UIDTraverser: UID lookup failed')
            return
        for brain in res:
            obj = brain.getObject()
            if obj is not None:
                return obj

        return