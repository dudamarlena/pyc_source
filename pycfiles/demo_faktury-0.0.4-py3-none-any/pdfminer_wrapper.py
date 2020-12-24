# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: <demo_faktury-0.0.4>\pdfminer_wrapper.py
# Compiled at: 2020-03-26 17:02:32
# Size of source mod 2**32: 1467 bytes


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
    laparams = LAParams()
    laparams.all_texts = True
    device = TextConverter(rsrcmgr, retstr, laparams=laparams)
    with open(path, 'rb') as (fp):
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        password = ''
        maxpages = 0
        caching = True
        pagenos = set()
        pages = PDFPage.get_pages(fp,
          pagenos,
          maxpages=maxpages,
          password=password,
          caching=caching,
          check_extractable=True)
        for page in pages:
            interpreter.process_page(page)

    device.close()
    str = retstr.getvalue()
    retstr.close()
    return str.encode('utf-8')