# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/test/test_thread.py
# Compiled at: 2013-04-11 17:47:52
import unittest
from camelot.view.model_thread import signal_slot_model_thread

class ModelThreadCase(unittest.TestCase):

    def test_task(self):

        def normal_request():
            pass

        task = signal_slot_model_thread.Task(normal_request)
        task.execute()

        def exception_request():
            raise Exception()

        task = signal_slot_model_thread.Task(exception_request)
        task.execute()

        def iterator_request():
            raise StopIteration()

        task = signal_slot_model_thread.Task(iterator_request)
        task.execute()

        def unexpected_request():
            raise SyntaxError()

        task = signal_slot_model_thread.Task(unexpected_request)
        task.execute()

    def test_task_handler(self):
        queue = [
         None, signal_slot_model_thread.Task(lambda : None)]
        task_handler = signal_slot_model_thread.TaskHandler(queue)
        task_handler.handle_task()
        self.assertEqual(len(queue), 0)
        return

    def test_model_thread(self):
        mt = signal_slot_model_thread.SignalSlotModelThread(lambda : None)
        mt.post(lambda : None)