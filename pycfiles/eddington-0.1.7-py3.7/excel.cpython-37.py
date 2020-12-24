# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/eddington/input/excel.py
# Compiled at: 2020-04-04 13:10:47
# Size of source mod 2**32: 432 bytes
import xlrd
from eddington.input.extraction import extract_data_from_rows

def read_data_from_excel(filepath, sheet):
    excel_obj = xlrd.open_workbook(filepath)
    sheet_obj = excel_obj.sheet_by_name(sheet)
    rows = [sheet_obj.row(i) for i in range(sheet_obj.nrows)]
    rows = [list(map(lambda element: element.value, row)) for row in rows]
    return extract_data_from_rows(rows=rows, file_name=(filepath.name), sheet=sheet)