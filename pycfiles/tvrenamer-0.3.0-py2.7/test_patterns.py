# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.cygwin-2.2.1-i686/egg/tvrenamer/tests/core/test_patterns.py
# Compiled at: 2015-11-08 18:30:19
from tvrenamer.core import patterns
from tvrenamer.tests import base

class PatternsTest(base.BaseTest):

    def test_get_expressions(self):
        exprs = patterns.get_expressions()
        self.assertEqual(len(exprs), 21)
        acopy = patterns.get_expressions()
        self.assertEqual(len(acopy), 21)
        self.assertEqual(exprs, acopy)