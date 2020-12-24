# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sorno/pdfutil.py
# Compiled at: 2019-08-09 12:21:44
# Size of source mod 2**32: 542 bytes
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals
import PyPDF2

def pdf_to_text(filepath):
    with open(filepath, 'rb') as (file_obj):
        pdf_reader = PyPDF2.PdfFileReader(file_obj)
        num_pages = pdf_reader.numPages
        count = 0
        text_segments = []
        while count < num_pages:
            text_segments.append(pdf_reader.getPage(count).extractText())
            count += 1

        return ''.join(text_segments)