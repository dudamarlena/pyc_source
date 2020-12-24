# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/collective/flowplayercaptions/extender.py
# Compiled at: 2011-01-03 17:11:02
from zope.component import adapts
from zope.interface import implements
from archetypes.schemaextender.interfaces import ISchemaExtender
from archetypes.schemaextender.field import ExtensionField
from plone.app.blob.field import BlobField
from collective.flowplayercaptions.interfaces import IFlowplayerCaptionsLayer
from Products.Archetypes import atapi
from collective.flowplayer.interfaces import IVideo
from collective.flowplayercaptions import captionsMessageFactory as _

class ExtensionBlobCaptionField(ExtensionField, BlobField):
    """ derivative of blobfield for extending schemas """
    pass


class CaptionsExtender(object):
    adapts(IVideo)
    implements(ISchemaExtender)
    fields = [
     ExtensionBlobCaptionField('captions', widget=atapi.FileWidget(label=_('Captions file'), description=_('caption_file_description', default='The captions file in Subrip format, to be used for captioning')), required=False, schemata='subtitles', validators='isNonEmptyFile')]

    def __init__(self, context):
        self.context = context

    def getFields(self):
        if IFlowplayerCaptionsLayer.providedBy(self.context.REQUEST):
            return self.fields
        return []