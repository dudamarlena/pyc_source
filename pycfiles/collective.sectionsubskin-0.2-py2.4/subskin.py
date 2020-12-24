# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/collective/sectionsubskin/browser/subskin.py
# Compiled at: 2008-07-18 06:49:04
try:
    from zope.publisher.browser import BrowserPage
except:
    from Products.Five.browser import BrowserView as BrowserPage

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.component import getAllUtilitiesRegisteredFor
from collective.sectionsubskin.interfaces import ISubskinDefinition

class SubSkin(BrowserPage):
    __module__ = __name__

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.subskin = None
        for layer in getAllUtilitiesRegisteredFor(ISubskinDefinition):
            if layer.type_interface.providedBy(request):
                self.subskin = layer

        return