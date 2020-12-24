# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/taurus/test/test_import.py
# Compiled at: 2019-08-19 15:09:30
"""Taurus import tests"""
from __future__ import absolute_import
import sys, unittest

class TaurusImportTestCase(unittest.TestCase):
    """
    Test if all the submodules can be imported
    """

    def setUp(self):
        """Preconditions: moduleexplorer utility has to be available """
        from .moduleexplorer import ModuleExplorer
        self.explore = ModuleExplorer.explore

    def testImportSubmodules(self):
        """
        Check that all taurus submodules import without problems

        Expected Results: It is expected to get no warning message
        on module importing
        """
        exclude_patterns = [
         'taurus\\.qt\\.qtgui\\.extra_.*',
         'taurus\\.qt\\.qtgui\\.qwt5',
         'taurus\\.external\\.qt\\.QtUiTools',
         'taurus\\.external\\.qt\\.Qwt5']
        try:
            import PyTango
        except ImportError:
            exclude_patterns.append('taurus\\.core\\.tango')

        try:
            import epics
        except ImportError:
            exclude_patterns.append('taurus\\.core\\.epics')

        moduleinfo, wrn = self.explore('taurus', verbose=False, exclude_patterns=exclude_patterns)
        msg = None
        if wrn:
            msg = '\n%s' % ('\n').join(list(zip(*wrn))[1])
        self.assertEqual(len(wrn), 0, msg=msg)
        return


if __name__ == '__main__':
    unittest.main()