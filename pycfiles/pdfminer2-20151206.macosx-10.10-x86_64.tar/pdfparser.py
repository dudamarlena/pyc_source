# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/chris/Projects/chris/various/pdfminer/venv/lib/python2.7/site-packages/pdfminer/pdfparser.py
# Compiled at: 2015-11-01 16:27:52
import logging
from io import BytesIO
from .psparser import PSStackParser
from .psparser import PSSyntaxError
from .psparser import PSEOF
from .psparser import KWD
from .settings import STRICT
from .pdftypes import PDFException
from .pdftypes import PDFStream
from .pdftypes import PDFObjRef
from .pdftypes import int_value
from .pdftypes import dict_value

class PDFSyntaxError(PDFException):
    pass


class PDFParser(PSStackParser):
    """
    PDFParser fetch PDF objects from a file stream.
    It can handle indirect references by referring to
    a PDF document set by set_document method.
    It also reads XRefs at the end of every PDF file.

    Typical usage:
      parser = PDFParser(fp)
      parser.read_xref()
      parser.read_xref(fallback=True) # optional
      parser.set_document(doc)
      parser.seek(offset)
      parser.nextobject()

    """

    def __init__(self, fp):
        PSStackParser.__init__(self, fp)
        self.doc = None
        self.fallback = False
        return

    def set_document(self, doc):
        """Associates the parser with a PDFDocument object."""
        self.doc = doc

    KEYWORD_R = KWD('R')
    KEYWORD_NULL = KWD('null')
    KEYWORD_ENDOBJ = KWD('endobj')
    KEYWORD_STREAM = KWD('stream')
    KEYWORD_XREF = KWD('xref')
    KEYWORD_STARTXREF = KWD('startxref')

    def do_keyword(self, pos, token):
        """Handles PDF-related keywords."""
        if token in (self.KEYWORD_XREF, self.KEYWORD_STARTXREF):
            self.add_results(*self.pop(1))
        elif token is self.KEYWORD_ENDOBJ:
            self.add_results(*self.pop(4))
        elif token is self.KEYWORD_NULL:
            self.push((pos, None))
        elif token is self.KEYWORD_R:
            try:
                (_, objid), (_, genno) = self.pop(2)
                objid, genno = int(objid), int(genno)
                obj = PDFObjRef(self.doc, objid, genno)
                self.push((pos, obj))
            except PSSyntaxError:
                pass

        elif token is self.KEYWORD_STREAM:
            (_, dic), = self.pop(1)
            dic = dict_value(dic)
            objlen = 0
            if not self.fallback:
                try:
                    objlen = int_value(dic['Length'])
                except KeyError:
                    if STRICT:
                        raise PDFSyntaxError('/Length is undefined: %r' % dic)

            self.seek(pos)
            try:
                _, line = self.nextline()
            except PSEOF:
                if STRICT:
                    raise PDFSyntaxError('Unexpected EOF')
                return

            pos += len(line)
            self.fp.seek(pos)
            data = self.fp.read(objlen)
            self.seek(pos + objlen)
            while 1:
                try:
                    linepos, line = self.nextline()
                except PSEOF:
                    if STRICT:
                        raise PDFSyntaxError('Unexpected EOF')
                    break

                if 'endstream' in line:
                    i = line.index('endstream')
                    objlen += i
                    if self.fallback:
                        data += line[:i]
                    break
                objlen += len(line)
                if self.fallback:
                    data += line

            self.seek(pos + objlen)
            logging.debug('Stream: pos=%d, objlen=%d, dic=%r, data=%r...', pos, objlen, dic, data[:10])
            obj = PDFStream(dic, data, self.doc.decipher)
            self.push((pos, obj))
        else:
            self.push((pos, token))
        return


class PDFStreamParser(PDFParser):
    """
    PDFStreamParser is used to parse PDF content streams
    that is contained in each page and has instructions
    for rendering the page. A reference to a PDF document is
    needed because a PDF content stream can also have
    indirect references to other objects in the same document.
    """

    def __init__(self, data):
        PDFParser.__init__(self, BytesIO(data))

    def flush(self):
        self.add_results(*self.popall())

    KEYWORD_OBJ = KWD('obj')

    def do_keyword(self, pos, token):
        if token is self.KEYWORD_R:
            try:
                (_, objid), (_, genno) = self.pop(2)
                objid, genno = int(objid), int(genno)
                obj = PDFObjRef(self.doc, objid, genno)
                self.push((pos, obj))
            except PSSyntaxError:
                pass

            return
        if token in (self.KEYWORD_OBJ, self.KEYWORD_ENDOBJ):
            if STRICT:
                raise PDFSyntaxError('Keyword endobj found in stream')
            return
        self.push((pos, token))