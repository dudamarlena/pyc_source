# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-intel/egg/tests/kyoka/callback/base_callback_test.py
# Compiled at: 2016-10-26 09:22:48
from tests.base_unittest import BaseUnitTest
from kyoka.callback.base_callback import BaseCallback
import sys, StringIO

class BaseCallbackTest(BaseUnitTest):

    def setUp(self):
        self.callback = BaseCallback()
        self.capture = StringIO.StringIO()
        sys.stdout = self.capture

    def tearDown(self):
        sys.stdout = sys.__stdout__

    def test_interrupt_gpi(self):
        self.false(self.callback.interrupt_gpi('dummy', 'dummy', 'dummy'))

    def test_define_log_tag(self):
        self.eq('BaseCallback', self.callback.define_log_tag())

    def test_log(self):
        self.callback.log('hoge')
        self.eq('[BaseCallback] hoge\n', self.capture.getvalue())