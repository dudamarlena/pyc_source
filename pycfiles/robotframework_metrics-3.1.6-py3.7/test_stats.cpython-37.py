# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\robotframework_metrics\test_stats.py
# Compiled at: 2020-03-14 04:42:30
# Size of source mod 2**32: 457 bytes
from robot.api import ResultVisitor

class TestStats(ResultVisitor):
    total_suite = 0
    passed_suite = 0
    failed_suite = 0

    def start_suite(self, suite):
        suite_test_list = suite.tests
        if not suite_test_list:
            pass
        else:
            self.total_suite += 1
            if suite.status == 'PASS':
                self.passed_suite += 1
            else:
                self.failed_suite += 1