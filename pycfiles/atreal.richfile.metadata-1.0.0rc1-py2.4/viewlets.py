# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/atreal/richfile/metadata/browser/viewlets.py
# Compiled at: 2009-09-04 10:38:20
from plone.app.layout.viewlets import ViewletBase
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.annotation.interfaces import IAnnotations
from atreal.richfile.qualifier.browser.viewlets import RichfileViewlet
from atreal.richfile.metadata.browser.controlpanel import IRichFileMetadataSchema
from atreal.richfile.metadata.interfaces import IMetadata
from atreal.richfile.metadata.interfaces import IMetadataExtractor
from atreal.richfile.metadata import RichFileMetadataMessageFactory as _

class MetadataViewlet(RichfileViewlet):
    """ """
    __module__ = __name__
    marker_interface = IMetadata
    plugin_interface = IMetadataExtractor
    plugin_id = 'metadata'
    plugin_title = 'Metadata'
    controlpanel_interface = IRichFileMetadataSchema

    @property
    def metadata(self):
        """ """
        info = IMetadataExtractor(self.context).info
        if info.has_key('metadata'):
            return info['metadata']
        else:
            return

    index = ViewPageTemplateFile('viewlet.pt')