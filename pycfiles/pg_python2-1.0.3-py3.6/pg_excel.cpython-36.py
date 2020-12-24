# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pg_python2/pg_excel.py
# Compiled at: 2018-08-03 06:01:13
# Size of source mod 2**32: 2115 bytes
import xlrd, logging, sys, json
try:
    xrange
except NameError:
    xrange = range

def read_excel_workbook(file_path):
    book = xlrd.open_workbook(file_path)
    logging.debug('The number of worksheets is {0}'.format(book.nsheets))
    logging.debug('Worksheet name(s): {0}'.format(book.sheet_names()))
    workbook_values = []
    num_sheets = book.nsheets
    if book.nsheets == 0:
        logging.error('No Sheets present in the file')
        return
    else:
        for sheet_idx in xrange(0, num_sheets):
            min_row_id = 999999
            max_row_id = 0
            min_col_id = 999999
            max_col_id = 0
            sh = book.sheet_by_index(sheet_idx)
            for row_id in xrange(0, sh.nrows):
                for col_id in xrange(0, sh.ncols):
                    if sh.cell_value(row_id, col_id) != xlrd.empty_cell.value:
                        if max_col_id < col_id:
                            max_col_id = col_id
                        else:
                            if min_col_id > col_id:
                                min_col_id = col_id
                            if max_row_id < row_id:
                                max_row_id = row_id
                        if min_row_id > row_id:
                            min_row_id = row_id

            sheet_matrix = []
            for row_id in xrange(min_row_id, max_row_id + 1):
                row_data = sh.row_slice(row_id, min_col_id, max_col_id + 1)
                row_values = []
                for data in row_data:
                    if data.value == xlrd.empty_cell.value:
                        row_values.append('')
                    else:
                        row_values.append(data.value)

                sheet_matrix.append(row_values)

            workbook_values.append(sheet_matrix)

        return json.dumps(workbook_values)


def log_helper():
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    root.addHandler(ch)


if __name__ == '__main__':
    log_helper()
    print(read_excel_workbook('./tests/Diarrhoea.xlsx'))