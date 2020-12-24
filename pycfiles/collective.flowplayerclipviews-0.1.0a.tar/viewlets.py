# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/collective/flowplayercaptions/browser/viewlets.py
# Compiled at: 2011-01-02 19:32:40
from plone.app.layout.viewlets import common
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

class VideoDataViewlet(common.ViewletBase):
    """A viewlet for captions data"""
    render = ViewPageTemplateFile('video_viewlet.pt')

    def url(self):
        return self.context.absolute_url()

    def captions_url(self):
        return self.context.absolute_url() + '/at_download/captions'