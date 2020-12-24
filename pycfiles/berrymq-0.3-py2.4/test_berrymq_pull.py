# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/tests/test_berrymq_pull.py
# Compiled at: 2009-08-15 20:04:46
import unittest
berrymq = None

class TestPriorityQueue(unittest.TestCase):
    __module__ = __name__

    def test_priority_queue(self):
        global berrymq
        queue = berrymq._PriorityQueue()
        queue.put('b', 10)
        queue.put('a', 5)
        self.assertEqual((5, 'a'), queue.get())
        self.assertEqual((10, 'b'), queue.get())


class TestQueue(unittest.TestCase):
    __module__ = __name__

    def setUp(self):
        try:
            import queue
        except ImportError:
            import Queue as queue

        self.queue = berrymq.Queue(None)
        self.queue._backend_queue = queue.Queue()
        return

    def test_empty_queue(self):
        self.assertEqual(0, self.queue.qsize())
        self.assert_(self.queue.empty())
        self.assert_(not self.queue.full())
        self.assertRaises(berrymq.Empty, self.queue.get, False)
        self.assertRaises(berrymq.Empty, self.queue.get_nowait)

    def test_not_empty_queue(self):
        self.queue._backend_queue.put((10, 'sampledata'))
        self.assertEqual(1, self.queue.qsize())
        self.assert_(not self.queue.empty())
        self.assert_(not self.queue.full())
        self.assertEqual('sampledata', self.queue.get())


class TestPullAPI(unittest.TestCase):
    __module__ = __name__

    def test_standalone_queue_object_api(self):
        queue = berrymq.Queue('pull_api2:*')
        berrymq.twitter('pull_api2:test', 'arg1', kwargs='kwargs')
        self.assertEqual(1, queue.qsize())
        message = queue.get()
        self.assertEqual('pull_api2', message.name)
        self.assertEqual(set(['test']), message.action)
        self.assertEqual('arg1', message.args[0])
        self.assertEqual('kwargs', message.kwargs['kwargs'])


def test_setup(berrymq_module):
    global berrymq
    berrymq = berrymq_module
    test_suite = unittest.TestSuite()
    test_suite.addTest(unittest.makeSuite(TestQueue))
    test_suite.addTest(unittest.makeSuite(TestPullAPI))
    return test_suite