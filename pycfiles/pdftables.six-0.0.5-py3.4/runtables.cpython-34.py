# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pdftables/runtables.py
# Compiled at: 2016-07-21 11:30:30
# Size of source mod 2**32: 3996 bytes
"""
Tell us what this does
"""
import os
from .pdftables import get_pdf_page, page_to_tables
from os.path import join, dirname
from . import pdftables_analysis as pta
from .display import to_string, get_dimensions
from io import StringIO
PDF_TEST_FILES = os.path.join(os.pardir, 'fixtures\\sample_data')
hints = []
SelectedPDF = '2012.01.PosRpt.pdf'
pagenumber = 1
hints = ['% Change', 'Uncommited']
SelectedPDF = 'AnimalExampleTables.pdf'
pagenumber = 2
filepath = os.path.join(PDF_TEST_FILES, SelectedPDF)
fh = open(filepath, 'rb')
pdf_page = get_pdf_page(fh, pagenumber)
table, diagnosticData = page_to_tables(pdf_page, extend_y=False, hints=hints, atomise=False)
fig, ax1 = pta.plotpage(diagnosticData)
result = StringIO()
columns, rows = get_dimensions(table)
result.write('     {} columns, {} rows\n'.format(columns, rows))
print(to_string(table))