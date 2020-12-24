# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pre/pd_params.py
# Compiled at: 2019-06-25 04:51:43
# Size of source mod 2**32: 487 bytes
"""
@author: magician
@file: pd_params.py
@date: 2019/06/05
"""
READ_FILE = {'xls': 'excel.pd_excel.read_excel', 
 'xlsx': 'excel.pd_excel.read_excel', 
 'csv': 'csv.pd_csv.read_csv', 
 'json': 'json.pd_json.read_json', 
 'zip': 'pickle.pd_zip.read_pickle'}
WRITE_FILE = {'xls': 'excel.pd_excel.write_excel', 
 'xlsx': 'excel.pd_excel.write_excel', 
 'csv': 'csv.pd_csv.write_csv', 
 'json': 'json.pd_json.write_json', 
 'zip': 'pickle.pd_zip.write_pickle'}