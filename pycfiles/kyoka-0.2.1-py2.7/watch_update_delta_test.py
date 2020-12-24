# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-intel/egg/tests/kyoka/finish_rule/watch_update_delta_test.py
# Compiled at: 2016-09-21 07:18:58
from tests.base_unittest import BaseUnitTest
from kyoka.finish_rule.watch_update_delta import WatchUpdateDelta
from nose.tools import raises

class WatchUpdateDeltaTest(BaseUnitTest):

    def test_satisfy_condition(self):
        rule = WatchUpdateDelta(patience=2, minimum_required_delta=2)
        self.false(rule.satisfy_condition('dummy', [1]))
        self.false(rule.satisfy_condition('dummy', [1, 2]))
        self.false(rule.satisfy_condition('dummy', [-1]))
        self.false(rule.satisfy_condition('dummy', [-1, -3]))
        self.false(rule.satisfy_condition('dummy', [1, -1]))
        self.true(rule.satisfy_condition('dummy', [1.9, -1]))

    def test_max_delta_memo_management(self):
        rule = WatchUpdateDelta(patience=2, minimum_required_delta=2)
        self.false(rule.satisfy_condition('dummy', [1.5]))
        self.include(1.5, rule.max_delta_memo)
        self.false(rule.satisfy_condition('dummy', [1, 2]))
        self.not_include(1.5, rule.max_delta_memo)

    def test_generate_progress_message(self):
        rule = WatchUpdateDelta(patience=2, minimum_required_delta=3)
        rule.satisfy_condition(1, [1.9, -1])
        msg = rule.generate_progress_message(5, 'dummy')
        self.include(str(5), msg)
        self.include(str(1), msg)

    def test_generate_finish_message(self):
        rule = WatchUpdateDelta(patience=2, minimum_required_delta=3)
        rule.satisfy_condition(1, [1.9, -1])
        msg = rule.generate_finish_message(5, 'dummy')
        self.include(str(2), msg)
        self.include(str(3), msg)
        self.include(str(1.9), msg)