# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/net/ossf/pdftotxt.py
# Compiled at: 2012-10-12 07:02:39
from coils.foundation import BLOBManager
from coils.foundation.api.pypdf import PdfFileReader
from filter import OpenGroupwareServerSideFilter

class PDFToTextOSSFilter(OpenGroupwareServerSideFilter):

    @property
    def handle(self):
        wfile = BLOBManager.ScratchFile()
        if self._mimetype not in 'application/pdf':
            raise Exception('Input stream is not a PDF document')
        self.log.debug('Reading PDF stream started')
        pdf = PdfFileReader(self._rfile)
        for i in range(0, pdf.getNumPages()):
            self.log.debug(('Reading text from page {0} of input stream').format(i))
            text = pdf.getPage(i).extractText().replace('\xa0', ' ')
            text = text.encode('ascii', 'xmlcharrefreplace')
            wfile.write(text)

        self.log.debug('Reading PDF stream complete')
        wfile.seek(0)
        return wfile

    @property
    def mimetype(self):
        return 'text/plain'