# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-intel/egg/iskra/audiofile/browser/listing.py
# Compiled at: 2012-07-09 11:41:45
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName
from Acquisition import aq_inner
from zope.publisher.browser import BrowserView
from iskra.audiofile.content import IAudioFile
from Products.ATContentTypes.interfaces.news import IATNewsItem

class AudioList(BrowserView):
    __call__ = ViewPageTemplateFile('listing.pt')

    def getAudioFiles(self):
        context = aq_inner(self.context)
        pc = getToolByName(context, 'portal_catalog')
        folder_path = ('/').join(context.getPhysicalPath())
        return pc(object_provides=IAudioFile.__identifier__, path={'query': folder_path, 'depth': 1})