# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/windmill/dep/_functest/reports.py
# Compiled at: 2011-01-13 01:48:00
import global_settings
all_tests_list = []

class FunctestReportInterface(object):
    """Simple class that returns a stub function if one of the methods isn't implemented"""

    def __getattr__(self, name):
        return lambda *args, **kwargs: None


class Report(object):

    def __init__(self):
        self.reporters = []

    def __getattr__(self, name):

        class ReporterWrapper(object):

            def __init__(self, name, reporters):
                self.name = name
                self.reporters = reporters

            def __call__(self, *args, **kwargs):
                for reporter in self.reporters:
                    getattr(reporter, self.name)(*args, **kwargs)

        return ReporterWrapper(name, self.reporters)

    def register_reporter(self, reporter):
        self.reporters.append(reporter)


report = Report()
register_reporter = report.register_reporter

def report_test_function(test_func):
    """Report a test function has finished"""
    getattr(report, test_func.test_type)(test_func)
    all_tests_list.append(test_func)


report_summary = report.report_summary

def report_summary(summary_dict, stdout_capture):
    """Report the test summmary at the end of a test run"""
    report.summary(all_tests_list, summary_dict, stdout_capture)


def report_final(totals):
    report.final(all_tests_list, totals)