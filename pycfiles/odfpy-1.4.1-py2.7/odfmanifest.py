# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/odf/odfmanifest.py
# Compiled at: 2020-01-18 11:47:38
from __future__ import print_function
import zipfile
from defusedxml.sax import make_parser
from xml.sax import handler
from xml.sax.xmlreader import InputSource
import xml.sax.saxutils
try:
    from cStringIO import StringIO
except ImportError:
    from io import StringIO

MANIFESTNS = 'urn:oasis:names:tc:opendocument:xmlns:manifest:1.0'

class ODFManifestHandler(handler.ContentHandler):
    """ The ODFManifestHandler parses a manifest file and produces a list of
        content """

    def __init__(self):
        self.manifest = {}
        self.elements = {(MANIFESTNS, 'file-entry'): (
                                      self.s_file_entry, self.donothing)}

    def handle_starttag(self, tag, method, attrs):
        method(tag, attrs)

    def handle_endtag(self, tag, method):
        method(tag)

    def startElementNS(self, tag, qname, attrs):
        method = self.elements.get(tag, (None, None))[0]
        if method:
            self.handle_starttag(tag, method, attrs)
        else:
            self.unknown_starttag(tag, attrs)
        return

    def endElementNS(self, tag, qname):
        method = self.elements.get(tag, (None, None))[1]
        if method:
            self.handle_endtag(tag, method)
        else:
            self.unknown_endtag(tag)
        return

    def unknown_starttag(self, tag, attrs):
        pass

    def unknown_endtag(self, tag):
        pass

    def donothing(self, tag, attrs=None):
        pass

    def s_file_entry(self, tag, attrs):
        m = attrs.get((MANIFESTNS, 'media-type'), 'application/octet-stream')
        p = attrs.get((MANIFESTNS, 'full-path'))
        self.manifest[p] = {'media-type': m, 'full-path': p}


def manifestlist(manifestxml):
    odhandler = ODFManifestHandler()
    parser = make_parser()
    parser.setFeature(handler.feature_namespaces, 1)
    parser.setContentHandler(odhandler)
    parser.setErrorHandler(handler.ErrorHandler())
    inpsrc = InputSource()
    if not isinstance(manifestxml, str):
        manifestxml = manifestxml.decode('utf-8')
    inpsrc.setByteStream(StringIO(manifestxml))
    parser.parse(inpsrc)
    return odhandler.manifest


def odfmanifest(odtfile):
    z = zipfile.ZipFile(odtfile)
    manifest = z.read('META-INF/manifest.xml')
    z.close()
    return manifestlist(manifest)


if __name__ == '__main__':
    import sys
    result = odfmanifest(sys.argv[1])
    for file in result.values():
        print('%-40s %-40s' % (file['media-type'], file['full-path']))