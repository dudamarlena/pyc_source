# uncompyle6 version 3.6.7
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: \Ft\Xml\XLink\Processor.py
# Compiled at: 2005-02-25 00:57:48
__doc__ = '\nXLink processing engine\n\nCopyright 2005 Fourthought, Inc. (USA).\nDetailed license and copyright information: http://4suite.org/COPYRIGHT\nProject home, documentation, distributions: http://4suite.org/\n'
from Ft.Xml.Domlette import NonvalidatingReader
from Ft.Xml.XLink import XLINK_NAMESPACE
from Ft.Xml.XLink import XLinkElements
__all__ = [
 'Processor']

class Processor:
    __module__ = __name__

    def run(self, iSrc):
        """
        Given an InputSource, reads the document, processing XLinks therein.

        Warning: The document will be modified in place.
        """
        document = NonvalidatingReader.parse(iSrc)
        xlinks = document.xpath('/descendant-or-self::*[@xlink:type]', explicitNss={'xlink': XLINK_NAMESPACE})
        for link in xlinks:
            xlink = XLinkElements.Create(link, iSrc)
            xlink.process()

        return document