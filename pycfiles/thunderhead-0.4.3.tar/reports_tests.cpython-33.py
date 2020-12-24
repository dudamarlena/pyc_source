# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/errr/programs/python/thunderhead/tests/reports_tests.py
# Compiled at: 2014-09-18 23:21:50
# Size of source mod 2**32: 1789 bytes
import vcr, tests
from thunderhead.builder import reports

class ReportTests(tests.VCRBasedTests):

    @vcr.use_cassette('get_report_list.yaml', cassette_library_dir=tests.fixtures_path, record_mode='once')
    def test_get_report_list(self):
        report_list = reports.get_report_list(tests.CONNECTION)
        self.assertIsInstance(report_list, list)

    @vcr.use_cassette('get_report_by_id.yaml', cassette_library_dir=tests.fixtures_path, record_mode='once')
    def test_get_report_by_id(self):
        report = reports.get_report(tests.CONNECTION, 1, date_from=2014091200, date_to=2014091800)
        self.assertIsNotNone(report)

    @vcr.use_cassette('get_report_by_id_bad_request.yaml', cassette_library_dir=tests.fixtures_path, record_mode='once')
    def test_get_report_by_id_bad_request(self):
        with self.assertRaises(reports.ReportException):
            reports.get_report(tests.CONNECTION, 1, date_from=2014091200, date_to=20140918)