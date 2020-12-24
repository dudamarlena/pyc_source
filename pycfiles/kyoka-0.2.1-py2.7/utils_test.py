# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-intel/egg/tests/kyoka/utils_test.py
# Compiled at: 2016-12-01 23:40:36
import kyoka.utils as U
from tests.base_unittest import BaseUnitTest

class UtilsTest(BaseUnitTest):

    def test_build_not_implemented_msg(self):
        message = U.build_not_implemented_msg(self, 'hoge')
        self.include('UtilsTest', message)
        self.include('hoge', message)

    def test_value_function_check(self):
        with self.assertRaises(TypeError) as (e):
            U.value_function_check('hoge', [BaseUnitTest, UtilsTest], 'value_function')
        self.include('hoge', e.exception.message)
        self.include('BaseUnitTest or UtilsTest', e.exception.message)