# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/test_stream/test_stream.py
# Compiled at: 2016-10-13 12:43:28
# Size of source mod 2**32: 494 bytes
import unittest
from mimo import Stream
from mimo.test_helper import TestHelper

class TestStream(unittest.TestCase):

    def test_run(self):
        stream = Stream(['a'], ['b'], fn=fn)
        helper = TestHelper(stream)
        self.assertEqual({'b': [2, 4, 6, 8, 10, 12, 14, 16, 18, 0]}, helper.run({'a': [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]}))


async def fn(ins, outs, state):
    async for item in ins.a:
                await outs.b.push(2 * item)


if __name__ == '__main__':
    unittest.main()