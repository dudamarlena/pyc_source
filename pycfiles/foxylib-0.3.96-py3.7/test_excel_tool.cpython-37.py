# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/foxylib/tools/software/microsoft/msoffice/tests/test_excel_tool.py
# Compiled at: 2020-01-28 20:08:02
# Size of source mod 2**32: 881 bytes
import logging, os
from unittest import TestCase
from foxylib.tools.log.foxylib_logger import FoxylibLogger
from foxylib.tools.software.microsoft.msoffice.excel_tool import ExcelTool
FILE_PATH = os.path.realpath(__file__)
FILE_DIR = os.path.dirname(FILE_PATH)

class TestExcelTool(TestCase):

    @classmethod
    def setUpClass(cls):
        FoxylibLogger.attach_stderr2loggers(logging.DEBUG)

    def test_01(self):
        logger = FoxylibLogger.func_level2logger(self.test_01, logging.DEBUG)
        filepath = os.path.join(FILE_DIR, '엑셀샘플.xls')
        workbook = ExcelTool.filepath2workbook(filepath)
        str_ll = list(ExcelTool.workbook_sheetname2line_iter(workbook, '함수목록'))
        self.assertTrue(str_ll)
        self.assertTrue(any((any(l) for l in str_ll)))
        for str_list in str_ll:
            logger.debug({'str_list': str_list})