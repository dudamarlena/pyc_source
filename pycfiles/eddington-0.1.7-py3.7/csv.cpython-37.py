# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/eddington/input/csv.py
# Compiled at: 2020-04-04 13:10:47
# Size of source mod 2**32: 295 bytes
import csv
from eddington.input.extraction import extract_data_from_rows

def read_data_from_csv(filepath):
    with open(filepath, mode='r') as (csv_file):
        csv_obj = csv.reader(csv_file)
        rows = list(csv_obj)
    return extract_data_from_rows(rows=rows, file_name=(filepath.name))