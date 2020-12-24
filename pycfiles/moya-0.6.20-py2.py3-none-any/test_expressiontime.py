# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/will/projects/moya/moya/tests/test_expressiontime.py
# Compiled at: 2016-12-08 16:29:22
import unittest
from moya.context import Context
from moya.context.expressiontime import ExpressionDateTime
from moya.compat import text_type
from moya import pilot
from moya.timezone import Timezone

class TestExpressionTime(unittest.TestCase):

    def setUp(self):
        self.context = Context()
        root = self.context.root
        root['now'] = ExpressionDateTime.utcnow()
        root['tz'] = Timezone('UTC')

    def test_str(self):
        text_type(self.context['.now'])

    def test_keys_values(self):
        with pilot.manage(self.context):
            self.context.eval('keys:.now')
            self.context.eval('values:.now')
            self.context.eval('items:.now')