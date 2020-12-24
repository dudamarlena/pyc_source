# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/test/test_test.py
# Compiled at: 2019-06-15 23:01:59
from unittest import TestCase
__author__ = 'Alexander.Li'
from filebeat_delegate import Configure

class TestTest(TestCase):

    def test_test(self):
        Configure.instance().parse('/Users/alex/workspace/filebeat_delegate/test/test.yml')
        self.assertTrue(True)