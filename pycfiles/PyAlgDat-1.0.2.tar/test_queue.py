# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/horn/Code/pythonprojects/py_alg_dat/testsuite/test_queue.py
# Compiled at: 2016-08-31 21:57:00
"""
Test Queue class.
"""
import unittest
from py_alg_dat import queue

class TestQueue(unittest.TestCase):
    """
    Test Queue class.
    """

    def setUp(self):
        self.queue1 = queue.Queue()
        self.queue1.enqueue(10)
        self.queue1.enqueue(20)
        self.queue1.enqueue(30)
        self.queue1.enqueue(40)
        self.queue1.enqueue(50)
        self.queue2 = queue.Queue()
        self.queue2.enqueue(10)
        self.queue2.enqueue(20)
        self.queue2.enqueue(30)
        self.queue2.enqueue(40)
        self.queue2.enqueue(50)
        self.queue3 = queue.Queue()
        self.queue3.enqueue(100)

    def test_queue_len(self):
        """
        Test operator "len".
        """
        self.assertEquals(5, len(self.queue1))

    def test_queue_equal(self):
        """
        Test operator "equal".
        """
        self.assertEquals(self.queue1, self.queue2)

    def test_queue_not_equal(self):
        """
        Test operator "inequal".
        """
        self.assertNotEquals(self.queue2, self.queue3)

    def test_queue_is_empty(self):
        """
        Test method "is_empty".
        """
        self.assertEquals(False, self.queue1.is_empty())

    def test_queue_clear(self):
        """
        Test method "clear".
        """
        self.queue1.clear()
        self.assertEquals(0, len(self.queue1))