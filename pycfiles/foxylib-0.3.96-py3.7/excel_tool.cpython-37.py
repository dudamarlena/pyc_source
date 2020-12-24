# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/foxylib/tools/software/microsoft/msoffice/excel_tool.py
# Compiled at: 2020-01-02 12:45:06
# Size of source mod 2**32: 1213 bytes
import xlrd
from future.utils import lmap

class ExcelTool:

    @classmethod
    def filepath2workbook(cls, filepath, *_, **__):
        return (xlrd.open_workbook)(filepath, *_, **__)

    @classmethod
    def workbook2sheetname_list(cls, workbook):
        return workbook.sheet_names()

    @classmethod
    def workbook_sheetname2line_iter(cls, workbook, sheetname):
        worksheet = workbook.sheet_by_name(sheetname)
        for row in worksheet.get_rows():
            value_list = lmap(lambda c: c.value, row)
            yield value_list

    @classmethod
    def workbook2line_iter(cls, workbook):
        for sheetname in cls.workbook2sheetname_list(workbook):
            yield from cls.workbook_sheetname2line_iter(workbook, sheetname)

        if False:
            yield None

    @classmethod
    def bytes2workbook(cls, bytes):
        return xlrd.open_workbook(file_contents=bytes)

    @classmethod
    def workbook2fulltext(cls, workbook):
        return '\n'.join([l for sheetname in cls.workbook2sheetname_list(workbook) for l in cls.workbook_sheetname2line_iter(workbook, sheetname)])