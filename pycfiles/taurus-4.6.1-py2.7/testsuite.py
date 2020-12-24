# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/taurus/test/testsuite.py
# Compiled at: 2019-08-19 15:09:30
"""
This module defines the test suite for the whole Taurus package
Usage::

  from taurus.test import testsuite
  testsuite.run()

"""
from __future__ import print_function
import os, sys, re, unittest, click, taurus
from taurus.external.qt import PYQT4
__docformat__ = 'restructuredtext'
PY3_EXCLUDED = ('unittest.loader._FailedTest.taurus.qt.qtgui.qwt5', 'unittest.loader._FailedTest.taurus.qt.qtgui.extra_sardana',
                'unittest.loader._FailedTest.taurus.qt.qtgui.extra_pool', 'unittest.loader._FailedTest.taurus.qt.qtgui.extra_macroexecutor')
ONLY_PYQT4 = ('unittest.loader._FailedTest.taurus.qt.qtgui.qwt5', )

def _filter_suite(suite, exclude_pattern, ret=None):
    """removes TestCases from a suite based on regexp matching on the Test id"""
    if ret is None:
        ret = unittest.TestSuite()
    for e in suite:
        if isinstance(e, unittest.TestCase):
            if e.__module__ == 'unittest.case':
                continue
            if sys.version_info.major > 2 and e.id() in PY3_EXCLUDED:
                print('Excluded %s' % e.id())
                continue
            if not PYQT4 and e.id() in ONLY_PYQT4:
                print('Excluded %s' % e.id())
                continue
            if re.match(exclude_pattern, e.id()):
                print('Excluded %s' % e.id())
                continue
            ret.addTest(e)
        else:
            _filter_suite(e, exclude_pattern, ret=ret)

    return ret


def get_taurus_suite(exclude_pattern='(?!)'):
    """discover all tests in taurus, except those matching `exclude_pattern`"""
    loader = unittest.defaultTestLoader
    start_dir = os.path.dirname(taurus.__file__)
    suite = loader.discover(start_dir, top_level_dir=os.path.dirname(start_dir))
    return _filter_suite(suite, exclude_pattern)


def run(disableLogger=True, exclude_pattern='(?!)'):
    """Runs tests for the taurus package"""
    if disableLogger:
        taurus.disableLogOutput()
    suite = get_taurus_suite(exclude_pattern=exclude_pattern)
    runner = unittest.TextTestRunner(descriptions=True, verbosity=2)
    return runner.run(suite)


@click.command('testsuite')
@click.option('--gui-tests/--skip-gui-tests', 'gui_tests', default=True, show_default=True, help='Perform tests requiring GUI')
@click.option('-e', '--exclude-pattern', 'exclude_pattern', default='(?!)', help="regexp pattern matching test ids to be excluded.\n    (e.g. 'taurus\\.core\\..*' would exclude taurus.core tests)\n    ")
def testsuite_cmd(gui_tests, exclude_pattern):
    """Launch the main test suite for Taurus'"""
    import taurus.test.skip
    taurus.test.skip.GUI_TESTS_ENABLED = gui_tests
    if not taurus.test.skip.GUI_TESTS_ENABLED:
        exclude_pattern = '(taurus\\.qt\\..*)|(%s)' % exclude_pattern
    else:
        exclude_pattern = exclude_pattern
    ret = run(exclude_pattern=exclude_pattern)
    if ret.wasSuccessful():
        exit_code = 0
    else:
        exit_code = 1
    sys.exit(exit_code)


if __name__ == '__main__':
    testsuite_cmd()