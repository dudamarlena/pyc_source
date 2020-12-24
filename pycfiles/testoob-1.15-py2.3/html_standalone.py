# uncompyle6 version 3.7.4
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/testoob/reporting/html_standalone.py
# Compiled at: 2009-10-07 18:08:46
"""Standalone HTML reporting, doesn't need external XSLT services"""
from base import BaseReporter

class OldHTMLReporter(BaseReporter):
    """Direct HTML reporting. Deprecated in favor of XSLT reporting"""
    __module__ = __name__

    def __init__(self, filename):
        BaseReporter.__init__(self)
        from cStringIO import StringIO
        self._sio = StringIO()
        from elementtree.SimpleXMLWriter import XMLWriter
        self.writer = XMLWriter(self._sio, 'utf-8')
        self.filename = filename
        self.test_starts = {}

    def start(self):
        BaseReporter.start(self)
        self._writeHeader()

    def _writeHeader(self):
        self.writer.start('html')
        self.writer.start('head')
        self.writer.element('title', 'TESTOOB unit-test report')
        self.writer.end('head')
        self.writer.start('body')
        self.writer.start('table', border='1')
        self.writer.start('tr')
        self.writer.element('td', 'Test Name')
        self.writer.element('td', 'Time')
        self.writer.element('td', 'Result')
        self.writer.element('td', 'More info')
        self.writer.end('tr')

    def done(self):
        BaseReporter.done(self)
        self.writer.end('table')
        self.writer.element('p', 'Total time: %.4f' % self.total_time)
        self.writer.end('body')
        self.writer.end('html')
        f = file(self.filename, 'w')
        try:
            f.write(self._getHtml())
        finally:
            f.close()

    def _getHtml(self):
        return self._sio.getvalue()

    def _encodeException(self, str):
        import re
        str = re.sub('File "(.+)",', '<a href="file:///\\1"> File "\\1",</a>', str)
        return str.replace('\n', '<br>')

    def startTest(self, test_info):
        BaseReporter.startTest(self, test_info)
        self.test_starts[test_info] = _time.time()

    def addError(self, test_info, err_info):
        BaseReporter.addError(self, test_info, err_info)
        self._add_unsuccessful_testcase('error', test_info, err_info)

    def addFailure(self, test_info, err_info):
        BaseReporter.addFailure(self, test_info, err_info)
        self._add_unsuccessful_testcase('failure', test_info, err_info)

    _SuccessTemplate = '<tr><td>%s</td><td>%s</td><td><font color="green">success</font></td></tr>'

    def addSuccess(self, test_info):
        BaseReporter.addSuccess(self, test_info)
        self._sio.write(HTMLReporter._SuccessTemplate % (str(test_info), self._test_time(test_info)))

    _SkipTemplate = '<tr><td>%s</td><td>%s</td><td><font color="blue">skipped</font></td><td>%s</td></tr>'

    def addSkip(self, test_info, err_info, isRegistered=True):
        BaseReporter.addSkip(self, test_info, err_info, isRegistered)
        self._sio.write(HTMLReporter._SkipTemplate % (str(test_info), self._test_time(test_info), str(err_info.exception_value())))

    _FailTemplate = '\n    <tr><td>%s</td><td>%s</td><td><font color="red">%s</font></td>\n    <td>%s</td></tr>\n    '

    def _add_unsuccessful_testcase(self, failure_type, test_info, err_info):
        self._sio.write(HTMLReporter._FailTemplate % (str(test_info), self._test_time(test_info), failure_type, self._encodeException(str(err_info))))

    def _test_time(self, test_info):
        result = _time.time() - self.test_starts[test_info]
        del self.test_starts[test_info]
        return '%.4f' % result