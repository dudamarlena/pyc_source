# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\xmind2Excel\libs\genexcel.py
# Compiled at: 2019-07-02 07:46:13
# Size of source mod 2**32: 2266 bytes
__author__ = '8034.com'
__date__ = '2018-10-22'
import sys, xlwt
from .xmindparse import XmindParse

class GenerateExcel(object):
    dist_excel_file = None
    excel_workbook = None

    def __init__(self, excel_path):
        self.excel_workbook = xlwt.Workbook()
        self.dist_excel_file = excel_path

    def genExcel(self, xmindParse):
        for name, sheet in xmindParse.generate_sheets():
            print('name={}, sheet= {}'.format(name, sheet))
            sheet_row_generator = xmindParse.parse_sheet(sheet)
            self.gen_sheet(name, sheet_row_generator)

        return self

    def gen_sheet(self, sheet_name, sheet_row_generator):
        print('新 sheet {}'.format(sheet_name))
        sheet_temp = self.excel_workbook.add_sheet(sheet_name)
        row = 1
        for row_info in sheet_row_generator:
            for col_num in range(len(row_info)):
                sheet_temp.write(row, col_num, row_info[col_num]['title'])

            row = row + 1

        return self

    def save(self):
        self.excel_workbook.save(self.dist_excel_file)
        return self

    def main(self, xmind_path):
        xmindParse = XmindParse(xmind_path)
        self.genExcel(xmindParse)
        self.save()
        return 'OK'


if __name__ == '__main__':
    xmind_path = 'D:\\CODE\\VScode\\workspace\\test01\\xmind2Excel\\xmind2Excel\\templet\\example_0.3.0.xmind'
    excel_path = 'D:\\CODE\\VScode\\workspace\\test01\\xmind2Excel\\xmind2Excel\\templet\\ttoo.xls'
    xmindParse = XmindParse(xmind_path)
    generateexcel = GenerateExcel(excel_path)
    generateexcel.genExcel(xmindParse)
    generateexcel.save()