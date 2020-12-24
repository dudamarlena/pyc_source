# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-intel/egg/tests/kyoka/algorithm/td_learning/base_td_method_test.py
# Compiled at: 2016-10-19 02:53:29
from tests.base_unittest import BaseUnitTest
from kyoka.algorithm.td_learning.base_td_method import BaseTDMethod
from kyoka.value_function.base_state_value_function import BaseStateValueFunction
from mock import Mock
from nose.tools import raises

class BaseTDMethodTest(BaseUnitTest):

    def setUp(self):
        self.algo = BaseTDMethod()

    @raises(TypeError)
    def test_reject_state_value_function(self):
        value_func = Mock(spec=BaseStateValueFunction)
        self.algo.update_value_function('dummy', 'dummy', value_func)