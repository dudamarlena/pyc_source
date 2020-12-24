# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/windmill/authoring/unit.py
# Compiled at: 2011-01-13 01:48:00
import unittest, sys
from windmill.dep import functest
reports = functest.reports

class UnitTestReporter(reports.FunctestReportInterface):

    def summary(self, test_list, totals_dict, stdout_capture):
        self.test_list = test_list


unittestreporter = UnitTestReporter()
reports.register_reporter(unittestreporter)

class WindmillUnitTestCase(unittest.TestCase):

    def setUp(self):
        import windmill
        windmill.stdout, windmill.stdin = sys.stdout, sys.stdin
        from windmill.bin.admin_lib import configure_global_settings, setup
        configure_global_settings()
        windmill.settings['TEST_URL'] = self.test_url
        if hasattr(self, 'windmill_settings'):
            for (setting, value) in self.windmill_settings.iteritems():
                windmill.settings[setting] = value

        self.windmill_shell_objects = setup()

    def testWindmill(self):
        self.windmill_shell_objects[('start_' + self.browser)]()
        self.windmill_shell_objects['do_test'](self.test_dir, threaded=False)
        for test in unittestreporter.test_list:
            self._testMethodDoc = getattr(test, '__doc__', None)
            self._testMethodName = test.__name__
            self.assertEquals(test.result, True)

        return

    def tearDown(self):
        from windmill.bin.admin_lib import teardown
        teardown(self.windmill_shell_objects)