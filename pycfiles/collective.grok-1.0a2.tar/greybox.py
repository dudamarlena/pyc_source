# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/collective/greybox/browser/greybox.py
# Compiled at: 2009-05-05 09:40:51
from Products.Five.browser import BrowserView
from collective.greybox.interfaces import IGreyBoxView
from zope.interface import implements

class greyBox(BrowserView):
    """
    perhaps we can readout some properties from a configlet....perhabs.
    """
    __module__ = __name__
    implements(IGreyBoxView)

    def getImages(self):
        context = self.context
        images = [ obj for obj in context.getFolderContents(full_objects=True) if obj.Type() == 'Image' ]
        return images

    def getOtherObjs(self):
        context = self.context
        others = [ obj for obj in context.getFolderContents() if obj.portal_type != 'Image' ]
        return others