# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/twisting/tests/test_base_worker.py
# Compiled at: 2009-03-28 16:00:34
import unittest
from twisted.internet import reactor
from twisting import ProgressManager, state_machine

class TestBaseWorker(unittest.TestCase):
    """
    """

    def setUp(self):
        """
        """
        self.__task_started = 0
        self.__task_finished = 0
        ProgressManager(all_finish_callback=self.all_finish_callback)

    def tearDown(self):
        """
        """
        pass

    def error_task_function(self, task):
        """
        """
        self.__task_started += 1
        assert self.__task_started == int(task.id_), '%s not %s' % (self.__task_started, task.id_)
        raise ValueError, 'Oups!'

    def task_function(self, task):
        """
        """
        self.__task_started += 1
        assert self.__task_started == int(task.id_), '%s not %s' % (self.__task_started, task.id_)
        return int(task.id_)

    def end_callback(self, result):
        """
        """
        self.__task_started -= 1
        assert self.__task_started == result, '%s not %s' % (self.__task_started, result)

    def error_callback(self, failure):
        """
        """
        reactor.stop()

    def all_finish_callback(self):
        """
        """
        assert self.__task_started == 0, '%s not %s' % (self.__task_started, 0)
        reactor.stop()

    def test_progress_base(self):
        """
        """
        initialized_ = ProgressManager().initialized
        assert initialized_, 'initialized_: %s' % initialized_
        pb1_ = ProgressManager()
        pb2_ = ProgressManager()
        assert pb1_ == pb2_, '%s not %s' % (pb1_, pb2_)

    def test_add_task(self):
        """
        """
        id_ = '1'
        pretty_name_ = 'task 1'
        added_ = ProgressManager().add_task(id_, pretty_name_)
        assert added_ == False, '%s not %s' % (added_, False)
        added_ = ProgressManager().add_task(id_, pretty_name_)
        assert added_ == True, '%s not %s' % (added_, False)
        started_ = ProgressManager().start_task(id_, worker_callback=None)
        assert started_ == False, '%s not %s' % (started_, False)
        started_ = ProgressManager().start_task(id_, worker_callback=self.task_function)
        assert started_ == True, '%s not %s' % (started_, True)
        id_ = '2'
        pretty_name_ = 'task 2'
        ProgressManager().add_task(id_, pretty_name_)
        started_ = ProgressManager().start_task(id_, worker_callback=self.task_function, end_callback=self.end_callback)
        assert started_ == True, '%s not %s' % (started_, True)
        id_ = '3'
        pretty_name_ = 'task 3'
        ProgressManager().add_task(id_, pretty_name_)
        started_ = ProgressManager().start_task(id_, worker_callback=self.error_task_function, end_callback=self.end_callback, error_callback=self.error_callback)
        assert started_ == True, '%s not %s' % (started_, True)
        reactor.run()
        return


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestBaseWorker, 'test_base_worker'))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')