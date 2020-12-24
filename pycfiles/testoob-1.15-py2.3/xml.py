# uncompyle6 version 3.7.4
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/testoob/reporting/xml.py
# Compiled at: 2009-10-07 18:08:46
"""Report results in XML format"""
from base import BaseReporter
import time

class XMLReporter(BaseReporter):
    """Reports test results in XML, in a format resembling Ant's JUnit xml
    formatting output."""
    __module__ = __name__

    def __init__(self):
        BaseReporter.__init__(self)
        from cStringIO import StringIO
        self._sio = StringIO()
        try:
            from elementtree.SimpleXMLWriter import XMLWriter
        except ImportError:
            from testoob.compatibility.SimpleXMLWriter import XMLWriter

        self.writer = XMLWriter(self._sio, 'utf-8')
        self.test_starts = {}

    def start(self):
        BaseReporter.start(self)
        self.writer.start('results')
        self.writer.start('testsuites')

    def done(self):
        BaseReporter.done(self)
        self.writer.element('total_time', value='%.4f' % self.total_time)
        self.writer.end('testsuites')
        if self.cover_amount is not None and self.cover_amount == 'xml':
            self._write_coverage(self.coverage)
        self.writer.end('results')
        return

    def get_xml(self):
        return self._sio.getvalue()

    def startTest(self, test_info):
        BaseReporter.startTest(self, test_info)
        self.test_starts[test_info] = time.time()

    def addError(self, test_info, err_info):
        BaseReporter.addError(self, test_info, err_info)
        self._add_unsuccessful_testcase('error', test_info, err_info)

    def addFailure(self, test_info, err_info):
        BaseReporter.addFailure(self, test_info, err_info)
        self._add_unsuccessful_testcase('failure', test_info, err_info)

    def _add_testcase_element(self, test_info, result, add_elements=lambda : None):
        self._start_testcase_tag(test_info)
        self.writer.element('result', result)
        add_elements()
        self.writer.end('testcase')

    def addSuccess(self, test_info):
        BaseReporter.addSuccess(self, test_info)
        self._add_testcase_element(test_info, 'success')

    def addSkip(self, test_info, err_info, isRegistered=True):
        BaseReporter.addSkip(self, test_info, err_info, isRegistered)

        def add_elements():
            self.writer.element('reason', err_info.exception_value())

        self._add_testcase_element(test_info, 'skip')

    def _add_unsuccessful_testcase(self, failure_type, test_info, err_info):

        def add_elements():
            """Additional elements specific for failures and errors"""
            self.writer.element(failure_type, str(err_info), type=err_info.exception_type(), message=err_info.exception_value())

        self._add_testcase_element(test_info, failure_type, add_elements)

    def _start_testcase_tag(self, test_info):
        self.writer.start('testcase', name=str(test_info), time=self._test_time(test_info))

    def _test_time(self, test_info):
        result = time.time() - self.test_starts[test_info]
        return '%.4f' % result

    def _write_coverage(self, coverage):
        self.writer.start('coverage')
        for (filename, stats) in coverage.getstatistics().items():
            self.writer.start('sourcefile', name=filename, statements=str(stats['lines']), executed=str(stats['covered']), percent=str(stats['percent']))
            (lines, covered) = coverage.coverage[filename].values()
            missing = [ line for line in covered if line not in lines ]
            self.writer.data(str(missing)[1:-1].replace(' ', ''))
            self.writer.end('sourcefile')

        self.writer.end('coverage')


class XMLFileReporter(XMLReporter):
    __module__ = __name__

    def __init__(self, filename):
        XMLReporter.__init__(self)
        self.filename = filename

    def done(self):
        XMLReporter.done(self)
        f = file(self.filename, 'w')
        try:
            f.write(self.get_xml())
        finally:
            f.close()