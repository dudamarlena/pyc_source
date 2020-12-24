# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-intel/egg/iskra/audiofile/content.py
# Compiled at: 2012-07-10 04:54:00
from plone.directives import form
from five import grok
from plone.multilingualbehavior import directives
from zope import schema
from Acquisition import aq_inner
from plone.namedfile.field import NamedImage, NamedFile
from iskra.audiofile import _
import os
from iskra.audiofile.interfaces import IMediaInfo

class IAudioFile(form.Schema):
    audiofile = NamedFile(title=_('File MP3'))
    audiofileogg = NamedFile(title=_('File Ogg'), required=False)
    directives.languageindependent('image')
    image = NamedImage(title=_('Image'))


class View(grok.View):
    grok.context(IAudioFile)
    grok.require('zope2.View')

    def video(self):
        info = IMediaInfo(self.context)
        return dict(title=self.context.Title(), description=self.context.Description(), height=info.height, width=info.width, duration=info.duration)

    def getFilename(self):
        context = aq_inner(self.context)
        return context.audiofile.filename