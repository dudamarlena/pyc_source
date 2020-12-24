# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\tests\simulation\test_throttling.py
# Compiled at: 2016-04-20 06:52:06
# Size of source mod 2**32: 2602 bytes
from unittest import TestCase
from mock import MagicMock, PropertyMock
from mad.simulation.tasks import TaskPool
from mad.simulation.throttling import NoThrottling, TailDrop
DUMMY_TASK = 'whatever'

class NoThrottlingTests(TestCase):

    def test_never_rejects(self):
        throttling = NoThrottling(MagicMock(TaskPool))
        self.assertTrue(throttling._accepts(DUMMY_TASK))


class TailDropTests(TestCase):

    def setUp(self):
        self.capacity = 50
        self.queue = MagicMock(TaskPool)
        self.pool_size(50)
        self.throttling = TailDrop(self.queue, self.capacity)

    def pool_size(self, length):
        type(self.queue).size = PropertyMock(return_value=length)

    def test_rejects_non_integer_capacity(self):
        try:
            capacity = 'not an integer'
            TailDrop(self.queue, capacity)
            self.fail('AssertionError expected!')
        except AssertionError as error:
            self.assertEqual(error.args[0], TailDrop.INVALID_CAPACITY.format(object=capacity))

    def test_rejects_negative_capacity(self):
        try:
            capacity = -5
            TailDrop(self.queue, capacity)
            self.fail('AssertionError expected!')
        except AssertionError as error:
            self.assertEqual(error.args[0], TailDrop.NEGATIVE_CAPACITY.format(capacity=capacity))

    def test_reject_at_capacity(self):
        self.pool_size(self.capacity)
        self.assertFalse(self.throttling._accepts(DUMMY_TASK))

    def test_reject_beyond_capacity(self):
        self.pool_size(self.capacity + 1)
        self.assertFalse(self.throttling._accepts(DUMMY_TASK))

    def test_accept_before_capacity(self):
        self.pool_size(self.capacity - 1)
        self.assertTrue(self.throttling._accepts(DUMMY_TASK))


if __name__ == '__main__':
    from unittest import main
    main()