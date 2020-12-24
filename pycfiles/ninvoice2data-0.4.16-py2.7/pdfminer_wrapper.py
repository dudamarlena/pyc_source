# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/ninvoice2data/input/pdfminer_wrapper.py
# Compiled at: 2019-02-01 05:18:39


def to_text(path):
    """Wrapper around `pdfminer`.

    Parameters
    ----------
    path : str
        path of electronic invoice in PDF

    Returns
    -------
    str : str
        returns extracted text from pdf

    """
    try:
        from StringIO import StringIO
        import sys
        reload(sys)
        sys.setdefaultencoding('utf8')
    except ImportError:
        from io import StringIO

    from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
    from pdfminer.converter import TextConverter
    from pdfminer.layout import LAParams
    from pdfminer.pdfpage import PDFPage
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    laparams.all_texts = True
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    with open(path, 'rb') as (fp):
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        password = ''
        maxpages = 0
        caching = True
        pagenos = set()
        pages = PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password, caching=caching, check_extractable=True)
        for page in pages:
            interpreter.process_page(page)

    device.close()
    str = retstr.getvalue()
    retstr.close()
    return str.encode('utf-8')