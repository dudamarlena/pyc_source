# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/test_report.py
# Compiled at: 2018-06-07 14:58:54
import pandas as pd
from pd_validator.validator import *
from pd_validator.schema import Schema
from pd_validator.report import Report
from pandas.testing import assert_frame_equal
df = pd.read_csv('../data/test_data.csv')
expected_report = pd.read_csv('../data/test_report.csv')
test_rules = {'col_1': {'dtype': int, 
             'length': 1, 
             'range': [
                     0, 1], 
             'required': True, 
             'codes': False, 
             'regex': False}, 
   'col_2': {'dtype': str, 
             'length': 1, 
             'range': False, 
             'required': False, 
             'codes': [
                     'A', 'B', 'C'], 
             'regex': False}}
test_schema = Schema(rules=test_rules)
actual_report = Report(df=df, schema=test_schema())
sort = [
 'inval_line', 'inval_col', 'inval_val', 'err_msg']

def test_report():
    assert_frame_equal(expected_report.sort_values(by=sort).reset_index(drop=True), actual_report().sort_values(by=sort).reset_index(drop=True))


if __name__ == '__main__':
    test_report()