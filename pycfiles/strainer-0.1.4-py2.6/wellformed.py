# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/strainer/wellformed.py
# Compiled at: 2011-03-21 01:30:30
"""Performs basic XHTML wellformedness checks."""
import xml.sax, xml.sax.handler, htmlentitydefs
from xml.sax._exceptions import SAXParseException
__all__ = [
 'is_wellformed_xml', 'is_wellformed_xhtml']
DOCTYPE_XHTML1_STRICT = '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">'

def is_wellformed_xhtml(docpart, record_error=None):
    """Calls is_wellformed_xml with doctype=DOCTYPE_XHTML1_STRICT
       and entitydefs=htmlentitydefs.entitydefs."""
    return is_wellformed_xml(docpart, doctype=DOCTYPE_XHTML1_STRICT, entitydefs=htmlentitydefs.entitydefs, record_error=record_error)


def is_wellformed_xml(docpart, doctype='', entitydefs={}, record_error=None):
    """Prefixes doctype to docpart and parses the resulting string.
       Returns True if it parses as XML without error. If entitydefs
       is given, checks that all named entity references are keys
       in entitydefs. Does not check against the external DTD declared
       in the doctype.

       If record_error is not None, it is called with the text of the
       first error message if there is one (that is, if this function
       will return False).
    """
    doc = doctype + docpart
    parser = xml.sax.make_parser()
    parser.setFeature(xml.sax.handler.feature_external_ges, False)
    parser.setFeature(xml.sax.handler.feature_external_pes, False)
    if entitydefs:

        class Handler(xml.sax.handler.ContentHandler):

            def skippedEntity(self, name):
                if name not in entitydefs:
                    raise SAXParseException('undefined entity', None, parser)
                return

        h = Handler()
        parser.setContentHandler(h)
    try:
        parser.feed(doc)
        parser.close()
        return True
    except SAXParseException, e:
        if record_error is not None:
            line, column = e.getLineNumber(), e.getColumnNumber()
            line -= doctype.count('\n')
            if line == 1:
                column -= len(doctype) - (doctype.rfind('\n') + 1)
            record_error('line %d, column %d: %s' % (line, column + 1, e.message))
        return False

    return


def test():
    assert is_wellformed_xhtml('<foo>&nbsp;&auml;&#65;</foo>')


if __name__ == '__main__':
    test()