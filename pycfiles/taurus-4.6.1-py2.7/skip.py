# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/taurus/test/skip.py
# Compiled at: 2019-08-19 15:09:30
"""This module provides utilities for skipping certain sets of tests"""
__docformat__ = 'restructuredtext'
import unittest
from taurus import tauruscustomsettings
from taurus import Logger

def skipUnlessGui():
    """Decorator to indicate that the given test should be skipped if GUI
    Tests are not enabled.

    It can be applied both to :class:`unittest.TestCase` classes and to
    test methods::

        class FooTest(unittest.TestCase):
            def test_something_which_does_not_need_gui()
                (...)

            @skipUnlessGui()
            def test_something_that requires_gui()
                (...)

        @skipUnlessGui()
        class GUITest(unittest.TestCase):
            (...)

    Note: using skipUnlessGui is equivalent to:

        @skipunless(taurus.test.GUI_TESTS_ENABLED, 'requires GUI')

    """
    Logger.deprecated(dep='skipUnlessGui', rel='4.0', alt='taurus testsuite --exclude-pattern')
    return unittest.skipUnless(GUI_TESTS_ENABLED, 'requires GUI')


def _hasgui():
    """Returns True if GUI is available. False otherwise
    The current implementation is not very robust: it just looks for the
    'DISPLAY' environment variable on posix systems and assumes True
    for other systems"""
    import os
    if os.name == 'posix' and not os.getenv('DISPLAY'):
        return False
    else:
        return True


GUI_TESTS_ENABLED = getattr(tauruscustomsettings, 'ENABLE_GUI_TESTS', _hasgui())