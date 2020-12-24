# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/tezign_zjj/PycharmProjects/autox/autox/model/model.py
# Compiled at: 2019-12-14 20:20:10
# Size of source mod 2**32: 726 bytes
"""
测试报告模板的对象
"""

class ReportModel:
    sum_report = []
    name = ''
    all_test = 0
    pass_test = 0
    fail_test = 0
    skip_test = 0
    total_run_time = ''

    def __init__(self, sum_report, name, all_test, pass_test, fail_test, skip_test, total_run_time):
        self.sum_report = []
        self.all_test = 0
        self.pass_test = 0
        self.fail_test = 0
        self.skip_test = 0
        self.sum_report = sum_report
        self.name = name
        self.all_test = all_test
        self.pass_test = pass_test
        self.fail_test = fail_test
        self.skip_test = skip_test
        self.total_run_time = total_run_time