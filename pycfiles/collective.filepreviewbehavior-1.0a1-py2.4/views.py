# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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