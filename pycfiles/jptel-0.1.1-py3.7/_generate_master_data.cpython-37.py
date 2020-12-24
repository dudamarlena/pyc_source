# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/jptel/data/_generate_master_data.py
# Compiled at: 2019-03-26 03:02:02
# Size of source mod 2**32: 1920 bytes
from jinja2 import Environment, PackageLoader
import requests, xlrd
xls_filenames = [
 '000124070.xls',
 '000124071.xls',
 '000124072.xls',
 '000124073.xls',
 '000124074.xls',
 '000124075.xls',
 '000124076.xls',
 '000124077.xls',
 '000124078.xls']
master_data_filename = 'area_code.py'
base_url = 'http://www.soumu.go.jp/main_content/'
sheet_name = '公開データ'
data_start_row = 2
row_area_code = 3
area_code_dict = {2:[],  3:[],  4:[],  5:[]}

def xls_download_from_MIS():
    for filename in xls_filenames:
        print('download {}'.format(filename))
        resp = requests.get(base_url + filename)
        if resp.status_code != 200:
            raise Exception('Excelファイルのダウンロードに失敗しました')
        with open(filename, 'wb') as (f):
            f.write(resp.content)


def read_xls_file(filename):
    print('reading {}'.format(filename))
    book = xlrd.open_workbook(filename)
    sheet = book.sheet_by_name(sheet_name)
    for index, row in enumerate(sheet.get_rows()):
        if index < data_start_row:
            continue
        area_code = row[row_area_code].value
        area_code_list = area_code_dict[len(area_code)]
        if area_code not in area_code_list:
            area_code_list.append(area_code)


def generate_master_data():
    print('generating {}'.format(master_data_filename))
    env = Environment(loader=(PackageLoader('__main__', '')))
    tmpl = env.get_template('master_data.tmpl')
    result = tmpl.render(area_code_dict=area_code_dict)
    with open(master_data_filename, 'w') as (f):
        f.write(result)


def main():
    for filename in xls_filenames:
        read_xls_file(filename)

    generate_master_data()


if __name__ == '__main__':
    main()