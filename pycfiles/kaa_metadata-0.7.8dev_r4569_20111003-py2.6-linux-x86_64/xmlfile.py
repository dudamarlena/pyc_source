# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /net/orion/data/home/tack/projects/kaa/metadata/build/lib.linux-x86_64-2.6/kaa/metadata/misc/xmlfile.py
# Compiled at: 2009-05-22 21:40:54
__all__ = [
 'Parser']
import os, sys, logging, xml.sax, kaa.metadata.core as core
log = logging.getLogger('metadata')
XML_TAG_INFO = {'image': 'Bins Image Description', 
   'album': 'Bins Album Description', 
   'freevo': 'Freevo XML Definition'}

class Identified:
    pass


class XML(core.Media):

    def __init__(self, file):
        ext = os.path.splitext(file.name)[1].lower()
        if ext not in ('.xml', '.fxd', '.html', '.htm'):
            raise core.ParseError()
        core.Media.__init__(self)
        self.mime = 'text/xml'
        self.type = ''
        if ext in ('.html', '.htm'):
            self.mime = 'text/html'
            self.type = 'HTML Document'
            return
        handler = xml.sax.ContentHandler()
        handler.startElement = self.startElement
        parser = xml.sax.make_parser()
        parser.setFeature('http://xml.org/sax/features/external-general-entities', False)
        parser.setContentHandler(handler)
        try:
            parser.parse(file)
        except Identified:
            pass
        except xml.sax.SAXParseException:
            raise core.ParseError()

    def startElement(self, name, attr):
        if name in XML_TAG_INFO:
            self.type = XML_TAG_INFO[name]
        else:
            self.type = 'XML file'
        raise Identified


Parser = XML