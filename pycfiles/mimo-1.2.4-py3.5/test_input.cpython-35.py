# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/test_connection/test_input.py
# Compiled at: 2016-10-13 12:43:28
# Size of source mod 2**32: 1226 bytes
import asyncio, unittest
from mimo.io.input import Input, InputClosed

class TestInput(unittest.TestCase):

    def setUp(self):
        self.loop = asyncio.get_event_loop()

    def test_push(self):
        connection = Input('a')
        self.loop.run_until_complete(connection.push(0))
        self.assertIn(0, connection._queue)

    def test_push_closed(self):
        connection = Input('a')
        connection.close()
        task = self.loop.create_task(connection.push(0))
        self.assertRaises(InputClosed, self.loop.run_until_complete, task)

    def test_peek(self):
        connection = Input('a')
        connection._queue.extend((0, 1, 2))
        task = self.loop.create_task(connection.peek())
        self.loop.run_until_complete(task)
        self.assertEqual(0, task.result())
        self.assertEqual([0, 1, 2], list(connection._queue))

    def test_pop(self):
        connection = Input('a')
        connection._queue.extend((0, 1, 2))
        task = self.loop.create_task(connection.pop())
        self.loop.run_until_complete(task)
        self.assertEqual(0, task.result())
        self.assertEqual([1, 2], list(connection._queue))


if __name__ == '__main__':
    unittest.main()