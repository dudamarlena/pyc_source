# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.6-i386/egg/collective/filepreviewbehavior/views.py
# Compiled at: 2010-01-11 09:34:53
from five import grok
from zope import interface
from plone.directives import dexterity
from Products import ARFilePreview
from collective.filepreviewbehavior.interfaces import IPreviewable

class PreviewProvider(dexterity.DisplayForm, ARFilePreview.views.PreviewProvider):
    __module__ = __name__
    grok.name('preview_provider')
    grok.context(IPreviewable)
    grok.template('fullview')
    grok.require('zope2.View')

    def __init__(self, *args, **kwargs):
        dexterity.DisplayForm.__init__(self, *args, **kwargs)
        ARFilePreview.views.PreviewProvider.__init__(self, *args, **kwargs)

    def __call__(self, *args, **kwargs):
        request = self.context.REQUEST
        if request.get('image', None):
            filename = request.get('image')
            (data, mime) = self.object.getSubObject(filename)
            response = request.RESPONSE
            response.setHeader('Content-Type', mime)
            return data
        return dexterity.DisplayForm.__call__(self, *args, **kwargs)


class FileAsDoc(dexterity.DisplayForm):
    __module__ = __name__
    grok.name('file_asdoc')
    grok.context(IPreviewable)
    grok.template('file_asdoc')
    grok.require('zope2.View')


class FilePreview(dexterity.DisplayForm):
    __module__ = __name__
    grok.name('file_preview')
    grok.context(IPreviewable)
    grok.template('file_preview')
    grok.require('zope2.View')