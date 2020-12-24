# uncompyle6 version 3.7.4
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/testoob/reporting/html.py
# Compiled at: 2009-10-07 18:08:46
"""
An HTML reporter.

Based on Wai Yip Tung's HTMLTestRunner:
http://tungwaiyip.info/software/HTMLTestRunner.html
"""
raise ImportError('HTMLTestRunner-based HTML reporting is still disabled')

def get_runner(title=None, report_attrs=[], description=None):
    import HTMLTestRunner
    return HTMLTestRunner.HTMLTestRunner(title=title, report_attrs=report_attrs, description=description)


from base import BaseReporter

class NewHTMLReporter(BaseReporter):
    """Creates an HTML file with the report"""
    __module__ = __name__

    def __init__(self, stream):
        BaseReporter.__init__(self)
        self.stream = stream
        self.success_count = 0
        self.failure_count = 0
        self.error_count = 0
        self.result = []

    def addSuccess(self, test_info):
        BaseReporter.addSuccess(self, test_info)
        self.success_count += 1
        self.result.append((0, test_info.classname(), '', ''))

    def addError(self, test_info, err_info):
        BaseReporter.addError(self, test_info, err_info)
        self.error_count += 1
        self.result.append((2, test_info.classname(), '', str(err_info)))

    def addFailure(self, test_info, err_info):
        BaseReporter.addFailure(self, test_info.classname(), err_info)
        self.failure_count += 1
        self.result.append((1, test_info.classname(), '', str(err_info)))

    def done(self):
        BaseReporter.done(self)
        runner = get_runner()
        import datetime
        runner.stopTime = datetime.datetime.now()
        self.stream.write(runner.generateReportString(self))