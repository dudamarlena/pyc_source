# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/jfurr/anouman/anouman/templates/test.py
# Compiled at: 2013-09-29 11:07:37
import random, unittest
from django.conf import settings
settings.configure()
from anouman.templates import commands

class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):
        self.seq = range(10)

    def test_shell_cmd_template(self):
        from test_expected_results import shell_commands_expected
        context = {'DOMAINNAME': 'example.com'}
        out = commands.render(context)
        self.assertTrue(out == shell_commands_expected)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestSequenceFunctions)
    unittest.TextTestRunner(verbosity=2).run(suite)