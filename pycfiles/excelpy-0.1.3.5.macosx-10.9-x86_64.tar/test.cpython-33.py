# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/edmondwells/venvs/excelpy/lib/python3.3/site-packages/excelpy/test.py
# Compiled at: 2014-03-05 09:15:44
# Size of source mod 2**32: 346 bytes
import shutil, os
from excelpy import ExcelPy
if __name__ == '__main__':
    try:
        shutil.rmtree('test_slayers')
        os.remove('test_slayers.xlsx')
    except:
        pass

    test_excel = shutil.copyfile('slayers.xlsx', 'test_slayers.xlsx')
    excel = ExcelPy(test_excel)
    excel.deleteSheet('Slayers')
    excel.save()