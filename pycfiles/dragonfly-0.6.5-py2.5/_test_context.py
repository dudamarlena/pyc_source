# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\dragonfly\grammar\_test_context.py
# Compiled at: 2009-03-19 11:51:25
import unittest
from dragonfly import Context, AppContext

class TestContextOperations(unittest.TestCase):

    def setUp(self):
        self.context_yes = Context()
        self.context_no = AppContext('never')

    def test_logic(self):
        self._check_match(self.context_yes, True)
        self._check_match(self.context_no, False)
        self._check_match(~self.context_yes, False)
        self._check_match(~self.context_no, True)
        self._check_match(self.context_yes & self.context_yes, True)
        self._check_match(self.context_yes & self.context_no, False)
        self._check_match(self.context_no & self.context_yes, False)
        self._check_match(self.context_no & self.context_no, False)
        self._check_match(self.context_yes | self.context_yes, True)
        self._check_match(self.context_yes | self.context_no, True)
        self._check_match(self.context_no | self.context_yes, True)
        self._check_match(self.context_no | self.context_no, False)
        self._check_match(self.context_yes & ~self.context_no, True)
        self._check_match(self.context_yes & ~self.context_yes, False)

    def _check_match(self, context, expected, executable='', title='', handle=None):
        self.assertEqual(context.matches(executable, title, handle), expected)


if __name__ == '__main__':
    unittest.main()