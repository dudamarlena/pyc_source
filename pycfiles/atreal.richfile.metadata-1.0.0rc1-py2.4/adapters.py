# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/atreal/richfile/metadata/adapters.py
# Compiled at: 2009-09-04 10:38:20
from zope.interface import implements
from Products.Archetypes.utils import shasattr
from atreal.filestorage.common.interfaces import IOmniFile
from atreal.richfile.qualifier.common import RFPlugin
from atreal.richfile.metadata.interfaces import IMetadataExtractor
from atreal.richfile.metadata.extractors import available_extractors, default_extractor

class MetadataExtractor(RFPlugin):
    """
    """
    __module__ = __name__
    implements(IMetadataExtractor)
    engine = 'plone'

    @property
    def contenttype(self):
        if shasattr(self, '_contenttype'):
            return self._contenttype
        self._contenttype = self.context.getContentType()
        return self._contenttype

    @property
    def extractors(self):
        """ """
        if shasattr(self, '_extractors'):
            return self._extractors
        self._extractors = []
        for extractor in available_extractors:
            x = extractor()
            if x.available() and self.contenttype in x.supportedMimetypes():
                self._extractors.append(x)

        return self._extractors

    def process(self):
        """ """
        if not self.isActive():
            return
        print 'MetadataExtractor processing ...'
        if not len(self.extractors):
            print 'No extractor found.'
            return
        metadata = self._extractMetadata()
        self.info['metadata'] = metadata

    def _extractMetadata(self):
        """ As it says in the title """
        print 'extractAndStoreMetadata'
        (extractor, default) = self._chooseExtractor()
        infile = IOmniFile(self.context.getFile())
        while True:
            metadata = extractor.extract(infile)
            if default:
                break
            if not metadata:
                (extractor, default) = self._chooseExtractor(used=extractor.__class__.__name__)
            else:
                break

        return metadata

    def _chooseExtractor(self, used=None):
        """ """
        for x in self.extractors:
            if used == x.__class__.__name__:
                continue
            if self.contenttype in x.bestMimetypes():
                return (
                 x, False)

        return (
         self.extractors[default_extractor], True)