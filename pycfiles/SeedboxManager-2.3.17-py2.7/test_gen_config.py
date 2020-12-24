# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.cygwin-1.7.35-i686/egg/seedbox/tests/test_gen_config.py
# Compiled at: 2015-06-14 13:30:57
"""Test cases for generating sample configs"""
from seedbox import options
from seedbox.tests import test

class ConfigTest(test.BaseTestCase):

    def test_list_common_opts(self):
        self.assertIsNotNone(options.list_opts())