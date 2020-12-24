# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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