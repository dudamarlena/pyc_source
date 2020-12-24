# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/dicom_tools/xlsReader.py
# Compiled at: 2018-05-21 04:28:19
# Size of source mod 2**32: 793 bytes
from __future__ import print_function
from openpyxl import load_workbook
from tabulate import tabulate

def xlsReader(filename, verbose=True):
    if verbose:
        print('xlsReader')
    wb = load_workbook(filename='responders.xlsx')
    sheet_names = wb.get_sheet_names()
    if verbose:
        print('sheet names:', sheet_names)
    results = []
    for sheet_name in sheet_names:
        if verbose:
            print('sheet name: ', sheet_name)
        sheet = wb.get_sheet_by_name(sheet_name)
        converted_sheet = []
        for row in sheet.rows:
            converted_row = []
            for cell in row:
                converted_row.append(cell.value)

            converted_sheet.append(converted_row)

        results.append(converted_sheet)

    return results