# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/atreal/richfile/metadata/extractors.py
# Compiled at: 2009-09-04 10:38:20
from zope.interface import implements
from atreal.richfile.metadata.interfaces import IExtractorWrapper
from Products.Archetypes.utils import OrderedDict
import StringIO
try:
    from hachoir_core.error import HachoirError
    from hachoir_core.cmd_line import unicodeFilename
    from hachoir_parser import guessParser
    from hachoir_metadata import extractMetadata
    from hachoir_core.stream import InputIOStream
    from atreal.richfile.metadata.extractors_mimetypes import HACHOIR_MT, HACHOIR_BEST_MT
    HACHOIR = True
except:
    HACHOIR = False

try:
    from atreal.richfile.metadata.lib.EXIF import process_file
    from atreal.richfile.metadata.extractors_mimetypes import EXIF_MT, EXIF_BEST_MT
    EXIF = True
except:
    EXIF = False

class BaseExtractor(object):
    """ A base class to wrapp extractor process """
    __module__ = __name__
    implements(IExtractorWrapper)
    mimetypes = []
    best_mimetypes = []

    def __init__(self):
        pass

    def available(self):
        """ True if the matching lib/binary is available"""
        raise NotImplemented('Subclass Responsiblity')

    def supportedMimetypes(self):
        """ Return the mimetypes list supported by the extractor """
        return self.mimetypes

    def bestMimetypes(self):
        """ Return the more effective mimetypes list supported by the extractor """
        return self.mimetypes

    def extract(self, myfile):
        """ Return a mapping filled with the file metadatas """
        raise NotImplemented('Subclass Responsiblity')


class HachoirExtractor(BaseExtractor):
    """ A metadata extractor based on Hachoir python lib from Haypo"""
    __module__ = __name__
    implements(IExtractorWrapper)

    def available(self):
        return HACHOIR

    def supportedMimetypes(self):
        return HACHOIR_MT

    def bestMimetypes(self):
        return HACHOIR_BEST_MT

    def extract(self, myfile):
        """ """
        if not self.available():
            return
        dataIO = myfile.open('r')
        filename, realname = unicodeFilename(myfile.name), myfile.name
        source = 'file:%s' % filename
        args = {'tags': [], 'filename': filename}
        stream = InputIOStream(dataIO, source=source, **args)
        parser = guessParser(stream)
        try:
            metadata = extractMetadata(parser)
        except HachoirError, err:
            print 'Metadata extraction error: %s' % unicode(err)
            metadata = None

        if not metadata:
            print 'Unable to extract metadata'
            dataIO.close()
            return
        dataIO.close()
        formated = metadata.exportPlaintext(line_prefix='')
        if not len(formated) or len(formated) == 1:
            return
        ordered = OrderedDict()
        for line in formated[1:]:
            item = line.split(':', 1)
            ordered[item[0]] = item[1]

        return ordered


class ExifExtractor(object):
    """ An extractor based one exif.py from Gene Cash and Ianaré Sévi """
    __module__ = __name__
    implements(IExtractorWrapper)
    mimetypes = []
    best_mimetypes = []

    def available(self):
        """ True if the matching lib/binary is available"""
        return EXIF

    def supportedMimetypes(self):
        """ Return the mimetypes list supported by the extractor """
        return EXIF_MT

    def bestMimetypes(self):
        """ Return the more effective mimetypes list supported by the extractor """
        return EXIF_BEST_MT

    def extract(self, myfile):
        """ Return a mapping filled with the file metadatas """
        if not self.available():
            return
        dataIO = myfile.open('r')
        result = process_file(dataIO, details=False, strict=False, debug=False)
        dataIO.close()
        if not result:
            print "%s doesn't provide metadata" % self.__class__.__name__
            return
        metadata = OrderedDict()
        keys = result.keys()
        keys.sort()
        for i in keys:
            if i in ('JPEGThumbnail', 'TIFFThumbnail'):
                continue
            metadata[i] = result[i].printable

        if 'JPEGThumbnail' in result:
            metadata['thumbnail'] = 'File has JPEG thumbnail'
        return metadata


available_extractors = [
 HachoirExtractor, ExifExtractor]
default_extractor = 0