# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\atapibasiclib\getfromxls.py
# Compiled at: 2019-12-24 05:59:18
# Size of source mod 2**32: 1096 bytes
import xlrd, os

def getdatafromxls(filename):
    file = xlrd.open_workbook(filename)
    table = file.sheet_by_name('testcases')
    rows = table.nrows
    cols = len(table.row_values(0))
    filedname_list = []
    for c in range(cols):
        filedname_list.append(table.row_values(0)[c])

    print('filedname_list=%s' % filedname_list)
    row_dict = {}
    table_list = list(range(rows - 1))
    for i in range(rows - 1):
        for j in range(cols):
            row_dict[filedname_list[j]] = table.row_values(i + 1)[j]

        table_list[i] = row_dict
        row_dict = {}

    return table_list


def get_case_data(filepath):
    book = xlrd.open_workbook(filepath)
    sheet = book.sheet_by_name('testcases')
    case = []
    for i in range(0, sheet.nrows):
        case.append(sheet.row_values(i))

    print('cases=%s' % case)
    return case


if __name__ == '__main__':
    get_case_data('../datafiles/basicApi.xlsx')