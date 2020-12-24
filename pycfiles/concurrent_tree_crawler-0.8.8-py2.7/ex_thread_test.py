# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/concurrent_tree_crawler/common/threads/test/ex_thread_test.py
# Compiled at: 2011-09-28 13:50:09
import unittest, threading
from concurrent_tree_crawler.common.threads.ex_thread import ExThread

class MyException(Exception):
    pass


class MyThread(ExThread):

    def __init__(self):
        ExThread.__init__(self)

    def run_with_exception(self):
        thread_name = threading.current_thread().name
        raise MyException(("An error in thread '{}'.").format(thread_name))


class ExThreadTestCase(unittest.TestCase):

    def test_basic(self):
        t = MyThread()
        t.start()
        self.assertRaises(MyException, t.join_with_exception)