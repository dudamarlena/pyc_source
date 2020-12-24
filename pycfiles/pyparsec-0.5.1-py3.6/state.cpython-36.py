# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/test/state.py
# Compiled at: 2015-11-14 12:05:31
# Size of source mod 2**32: 531 bytes
import unittest
from parsec import *
sample = 'It is a simple string.'

class TestState(unittest.TestCase):

    def test_next(self):
        st = BasicState(sample)
        for i in range(len(sample)):
            idx = st.index
            re = st.next()
            self.assertEqual(re, st.data[idx])

        with self.assertRaises(Exception) as (err):
            st.next()
        self.assertTrue(issubclass(type(err.exception), ParsecEof))


if __name__ == '__main__':
    unittest.main()