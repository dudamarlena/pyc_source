# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/hepdata_converter/testsuite/test_optioninitmixin.py
# Compiled at: 2020-03-05 14:33:22
import unittest
from hepdata_converter.common import OptionInitMixin, Option

class OptionInitMixinTestSuite(unittest.TestCase):

    def test_dir(self):

        class TestClass(OptionInitMixin):

            @classmethod
            def options(cls):
                return {'testoption': Option('testoption')}

            def __init__(self, *args, **kwargs):
                OptionInitMixin.__init__(self, options=kwargs)

        test_value = 1
        a = TestClass(testoption=test_value)
        self.assertEqual(a.testoption, test_value)
        self.assertIn('testoption', dir(a))