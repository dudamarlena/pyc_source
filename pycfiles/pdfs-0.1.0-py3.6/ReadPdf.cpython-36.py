# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pdfs/ReadPdf.py
# Compiled at: 2017-08-14 16:20:11
# Size of source mod 2**32: 1394 bytes
import hashlib
from io import StringIO
from functools import lru_cache
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from unidecode import unidecode
from .Cache import cachedRequest
from .Exceptions import UserException

def getPdfTxt(fname):
    return _getPdf(fname, cache_key=(md5sum(fname)))


@cachedRequest('PDF')
def _getPdf(fname, cache_key=None):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    fp = open(fname, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ''
    maxpages = 0
    caching = True
    pagenos = set()
    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password, caching=caching, check_extractable=True):
        interpreter.process_page(page)
        print('\x0c', file=retstr)

    text = retstr.getvalue()
    fp.close()
    device.close()
    retstr.close()
    return [unidecode(x) for x in text.split('\x0c') if x.strip()]


@lru_cache(maxsize=32)
def md5sum(fname):
    try:
        return hashlib.md5(open(fname, 'rb').read()).hexdigest()
    except FileNotFoundError:
        raise UserException('File {} not found'.format(fname))