# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/nti/nose_traceback_info/tests/test_nose_traceback_info.py
# Compiled at: 2015-04-21 14:22:59
"""

$Id$
"""
from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = b'restructuredtext en'
logger = __import__(b'logging').getLogger(__name__)
import sys
from unittest import TestCase, TestSuite
from nti.nose_traceback_info import NoseTracebackInfoPlugin
from nose.plugins import PluginTester
from nose.proxy import ResultProxy

class TestNoseTracebackInfoPlugin(PluginTester, TestCase):
    activate = b'--with-traceback-info'
    plugins = [NoseTracebackInfoPlugin()]
    ignoreFiles = True

    def test_format_failure(self):
        formatted = str(self.output)
        __traceback_info__ = formatted
        lines = formatted.split(b'\n' if isinstance(formatted, bytes) else b'\n')
        self.assertEqual(lines[(-8)].strip(), b'ValueError')
        self.assertEqual(lines[(-9)].strip()[0:27], b'- __traceback_info__: Child')

    def makeSuite(self):
        caller = sys._getframe(1)
        config = caller.f_locals[b'conf']

        class TC(TestCase):

            def runTest(self):
                __traceback_info__ = b'Childâ\x80\x99s'
                raise ValueError

        class Suite(TestSuite):

            def run(self, result, debug=False):
                result = ResultProxy(result, self._tests[0], config)
                return super(Suite, self).run(result, debug=debug)

        return Suite([TC()])


class TestNoseTracebackInfoDirectly(TestCase):

    def _check(self):
        plugin = NoseTracebackInfoPlugin()
        _, tb, _ = plugin.formatFailure(None, sys.exc_info())
        if isinstance(str(b''), bytes):
            assert isinstance(tb, bytes)
        else:
            assert isinstance(tb, str)
        return

    def test_unicode_decoding(self):
        try:
            __traceback_info__ = b'Childs \xff\xfe=\xd8\xa9\xdc'
            raise ValueError
        except ValueError:
            self._check()

        try:
            __traceback_info__ = b'Childs 💩'
            raise ValueError
        except ValueError:
            self._check()