# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/zyklus/test_zyklus.py
# Compiled at: 2018-01-21 10:58:32
from zyklus import Zyklus
import unittest, time

class HelperObj(object):

    def __init__(self, initial):
        self.curr = initial

    def add(self, what):
        self.curr += what

    def multiply(self, what):
        self.curr = self.curr * what

    def result(self):
        return self.curr


import threading

class ZyklusTest(unittest.TestCase):

    def setUp(self):
        self.zyklus = Zyklus()
        self.zyklusThread = threading.Thread(target=self.zyklus.loop)
        self.zyklusThread.start()
        self.helperObj = HelperObj(2)

    def tearDown(self):
        self.zyklus.terminate()

    def test_loop(self):
        self.zyklus.post(lambda : self.helperObj.add(1))
        time.sleep(0.1)
        self.assertEqual(3, self.helperObj.result())
        self.zyklus.post(lambda : self.helperObj.add(1))
        self.zyklus.post(lambda : self.helperObj.add(1))
        time.sleep(0.1)
        self.assertEqual(5, self.helperObj.result())

    def test_terminate(self):
        self.zyklus.terminate()
        initial = self.helperObj.result()
        self.zyklus.post(lambda : self.helperObj.add(1))
        time.sleep(0.1)
        self.assertEqual(initial, self.helperObj.result())
        self.assertFalse(self.zyklusThread.isAlive())
        self.assertTrue(self.zyklus.terminated)

    def test_post(self):
        target = self.helperObj
        self.zyklus.post(lambda : target.add(1))
        self.zyklus.post(lambda : target.multiply(2))
        time.sleep(0.1)
        self.assertEqual(target.result(), 6)
        try:
            self.zyklus.post(self.helperObj)
            raise AssertionError()
        except AssertionError:
            pass

    def test_is_callable(self):
        self.assertTrue(Zyklus.is_callable(lambda a: 1))
        self.assertFalse(Zyklus.is_callable(self.helperObj))
        self.helperObj.__call__ = lambda a, b: 1
        self.assertTrue(Zyklus.is_callable(self.helperObj))

    def test_ensure_postable(self):
        try:
            self.zyklus.ensure_postable(self.helperObj)
            raise AssertionError()
        except AssertionError:
            pass

        self.assertTrue(self.zyklus.ensure_postable(lambda : 1))

    def test_post_delayed(self):
        initialValue = self.helperObj.result()
        expectedResult = (initialValue + 5) * 10
        self.zyklus.post_delayed(lambda : self.helperObj.multiply(10), 0.2)
        self.zyklus.post_delayed(lambda : self.helperObj.add(5), 0.1)
        self.assertEqual(initialValue, self.helperObj.result())
        time.sleep(0.4)
        self.assertEqual(expectedResult, self.helperObj.result())

    def test_post_delayed_cancellation(self):
        initialValue = self.helperObj.result()
        expectedResult = initialValue + 5
        multPost = self.zyklus.post_delayed(lambda : self.helperObj.multiply(10), 0.2)
        self.zyklus.post_delayed(lambda : self.helperObj.add(5), 0.1)
        self.assertEqual(initialValue, self.helperObj.result())
        multPost.cancel()
        time.sleep(0.4)
        self.assertEqual(expectedResult, self.helperObj.result())

    def test_exec_callable(self):
        self.zyklus.exec_callable(lambda : self.helperObj.add(9))
        self.assertEqual(11, self.helperObj.result())